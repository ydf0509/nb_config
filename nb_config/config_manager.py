"""
nb_config 通用配置管理器
统一处理配置文件的查找、创建、导入、合并等逻辑
解决 nb_log、funboost 等项目中重复的配置管理代码
"""

import sys
import os
import importlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from shutil import copyfile


class ConfigManager:
    """
    通用配置管理器
    
    统一处理：
    1. 智能配置文件查找（脚本目录 > 项目根目录 > PYTHONPATH）
    2. 自动配置文件创建
    3. 动态导入和热重载
    4. 配置合并和验证
    5. 环境检查和详细错误提示
    """
    
    def __init__(
        self,
        config_name: str,
        target_module: Optional[str] = None,
        default_config_path: Optional[str] = None,
        auto_create: bool = True,
        config_class_names: Optional[List[str]] = None,
        search_paths: Optional[List[str]] = None
    ):
        """
        初始化配置管理器
        
        Args:
            config_name: 配置文件名（不含.py后缀），如 'funboost_config'
            target_module: 目标模块路径，如 'funboost.config'  
            default_config_path: 默认配置模板路径
            auto_create: 是否自动创建配置文件
            config_class_names: 需要合并的配置类名列表
            search_paths: 自定义搜索路径列表
        """
        self.config_name = config_name
        self.target_module = target_module
        self.default_config_path = default_config_path
        self.auto_create = auto_create
        self.config_class_names = config_class_names or []
        
        # 配置文件搜索路径（优先级从高到低）
        self.search_paths = search_paths or self._get_default_search_paths()
        
        # 缓存
        self._loaded_config = None
        self._config_file_path = None
    
    def _get_default_search_paths(self) -> List[str]:
        """获取默认的配置文件搜索路径"""
        paths = []
        
        # 1. 当前脚本所在目录
        if sys.path and sys.path[0]:
            current_script_path = Path(sys.path[0]).resolve()
            paths.append(str(current_script_path))
        
        # 2. 项目根目录
        if len(sys.path) > 1 and sys.path[1]:
            project_root_path = Path(sys.path[1]).resolve()
            paths.append(str(project_root_path))
        
        # 3. 其他 PYTHONPATH 目录
        for path in sys.path[2:]:
            if path and not self._is_system_path(path):
                paths.append(str(Path(path).resolve()))
        
        return paths
    
    def _is_system_path(self, path: str) -> bool:
        """判断是否为系统路径（不应该在其中创建配置文件）"""
        system_indicators = [
            '/lib/python', r'\lib\python',
            '.zip', '.egg',
            'site-packages',
            '/usr/', r'\Python',
        ]
        return any(indicator in path for indicator in system_indicators)
    
    def find_config_file(self) -> Optional[str]:
        """查找配置文件，返回找到的文件路径"""
        config_filename = f"{self.config_name}.py"
        
        for search_path in self.search_paths:
            config_path = Path(search_path) / config_filename
            if config_path.exists():
                self._config_file_path = str(config_path)
                return self._config_file_path
        
        return None
    
    def create_config_file(self, target_path: Optional[str] = None) -> str:
        """
        创建配置文件
        
        Args:
            target_path: 目标路径，如果为None则使用第一个有效的搜索路径
            
        Returns:
            创建的配置文件路径
        """
        if not self.auto_create:
            raise RuntimeError("自动创建配置文件功能已禁用")
        
        # 确定创建位置
        if target_path:
            create_path = Path(target_path)
        else:
            create_path = self._get_best_create_path()
        
        config_filename = f"{self.config_name}.py"
        config_file_path = create_path / config_filename
        
        # 创建目录（如果不存在）
        create_path.mkdir(parents=True, exist_ok=True)
        
        # 复制默认配置文件或生成基础配置
        if self.default_config_path and Path(self.default_config_path).exists():
            copyfile(self.default_config_path, config_file_path)
        else:
            self._generate_basic_config(config_file_path)
        
        self._config_file_path = str(config_file_path)
        print(f"✅ 已在 {config_file_path} 创建配置文件")
        
        return self._config_file_path
    
    def _get_best_create_path(self) -> Path:
        """获取最佳的配置文件创建路径"""
        for search_path in self.search_paths:
            path = Path(search_path)
            if not self._is_system_path(search_path) and path.exists():
                return path
        
        # 如果都不合适，抛出错误并提供详细指导
        self._raise_pythonpath_error()
    
    def _generate_basic_config(self, config_file_path: Path):
        """生成基础配置文件"""
        content = f'''"""
{self.config_name} 配置文件
由 nb_config 自动生成
"""

'''
        
        # 如果指定了目标模块，尝试生成装饰器模板
        if self.target_module:
            content += f'''from nb_config import nb_config_class

@nb_config_class('{self.target_module}')
class Config:
    # 在这里添加你的配置项
    # 例如：
    # database_url = 'your-database-url'
    # debug = True
    pass
'''
        else:
            content += '''# 在这里添加你的配置项
# 例如：
# DATABASE_URL = 'your-database-url'
# DEBUG = True
'''
        
        with open(config_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def load_config(self, reload: bool = False) -> Any:
        """
        加载配置文件
        
        Args:
            reload: 是否强制重新加载
            
        Returns:
            配置模块对象
        """
        if self._loaded_config and not reload:
            return self._loaded_config
        
        # 查找配置文件
        config_path = self.find_config_file()
        
        if not config_path:
            if self.auto_create:
                print(f"💡 未找到 {self.config_name}.py 配置文件，正在自动创建...")
                self.create_config_file()
            else:
                self._raise_config_not_found_error()
        
        # 导入配置模块
        try:
            config_module = importlib.import_module(self.config_name)
            if reload:
                importlib.reload(config_module)
            
            self._loaded_config = config_module
            
            # 如果指定了目标模块，执行配置合并
            if self.target_module:
                self._merge_config_to_target(config_module)
            
            print(f"✅ 已加载配置文件: {self._config_file_path}")
            return config_module
            
        except Exception as e:
            raise ImportError(f"加载配置文件失败: {e}")
    
    def _merge_config_to_target(self, config_module: Any):
        """将用户配置合并到目标模块（用于兼容旧版本使用方式）"""
        try:
            target_module = importlib.import_module(self.target_module)
            
            # 合并指定的配置类
            for class_name in self.config_class_names:
                if hasattr(config_module, class_name) and hasattr(target_module, class_name):
                    user_config = getattr(config_module, class_name)()
                    target_config = getattr(target_module, class_name)
                    
                    # 假设目标配置类有 update_cls_attribute 方法
                    if hasattr(target_config, 'update_cls_attribute'):
                        target_config.update_cls_attribute(**user_config.get_dict())
                    
        except Exception as e:
            print(f"⚠️  配置合并警告: {e}")
    
    def _raise_config_not_found_error(self):
        """抛出配置文件未找到的详细错误"""
        search_info = "\n".join([f"  • {path}" for path in self.search_paths])
        
        raise FileNotFoundError(f'''
❌ 未找到配置文件: {self.config_name}.py

🔍 已在以下路径搜索:
{search_info}

💡 解决方案:
1. 在上述任一路径创建 {self.config_name}.py 文件
2. 或设置 auto_create=True 启用自动创建
3. 或确保配置文件在 PYTHONPATH 中

📚 PYTHONPATH 基础知识:
https://github.com/ydf0509/pythonpathdemo
        ''')
    
    def _raise_pythonpath_error(self):
        """抛出 PYTHONPATH 配置错误"""
        raise EnvironmentError(f'''
❌ 无法找到合适的配置文件创建位置

🔍 当前 PYTHONPATH 路径:
{chr(10).join(f"  {i+1}. {path}" for i, path in enumerate(sys.path))}

💡 解决方案:
请在运行脚本前设置 PYTHONPATH 为你的项目根目录:

Linux/Mac:
export PYTHONPATH=/path/to/your/project

Windows CMD:
set PYTHONPATH=C:\\path\\to\\your\\project

Windows PowerShell:
$env:PYTHONPATH = "C:\\path\\to\\your\\project"

📚 深入理解 PYTHONPATH:
https://github.com/ydf0509/pythonpathdemo

⚠️  注意: 请使用临时环境变量，不要在系统配置文件中永久设置
        ''')


# 便捷函数
def auto_load_config(
    config_name: str,
    target_module: Optional[str] = None,
    **kwargs
) -> Any:
    """
    便捷的配置加载函数
    
    Args:
        config_name: 配置文件名
        target_module: 目标模块路径
        **kwargs: 其他 ConfigManager 参数
        
    Returns:
        配置模块对象
    """
    manager = ConfigManager(
        config_name=config_name,
        target_module=target_module,
        **kwargs
    )
    return manager.load_config() 