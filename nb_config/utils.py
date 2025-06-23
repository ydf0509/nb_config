"""
nb_config 工具函数
提供一些实用的配置管理和调试功能
"""

import importlib
import inspect
from typing import Any, List, Dict
from .simple_data_class import DataClassBase


def print_dataclass_configs(module_path: str, indent: int = 4) -> None:
    """
    打印指定模块下所有 DataClassBase 子类的 get_pwd_enc_json() 输出
    
    Args:
        module_path: 模块路径，如 'your_project.config'
        indent: JSON 缩进级别，默认为 4
        
    Example:
        ```python
        from nb_config.utils import print_dataclass_configs
        
        # 打印配置模块中所有配置类的加密JSON
        print_dataclass_configs('tests.mock_sitepackage.config_default')
        ```
    """
    try:
        # 导入目标模块
        target_module = importlib.import_module(module_path)
        
        # 获取模块中所有的 DataClassBase 子类
        dataclass_classes = find_dataclass_subclasses(target_module)
        
        if not dataclass_classes:
            print(f"📋 模块 {module_path} 中未找到 DataClassBase 子类")
            return
        
        print(f"🔍 模块 {module_path} 中的 DataClassBase 配置类:")
        print("=" * 60)
        
        for class_name, class_obj in dataclass_classes.items():
            try:
                # 创建类实例（如果可能）
                instance = class_obj()
                
                print(f"\n📦 配置类: {class_name}")
                print(f"🔒 加密JSON输出:")
                print(instance.get_pwd_enc_json(indent=indent))
                
            except Exception as e:
                print(f"\n⚠️  无法实例化配置类 {class_name}: {e}")
                # 尝试直接从类属性获取信息
                print(f"📋 类属性信息:")
                class_attrs = {k: v for k, v in class_obj.__dict__.items() 
                             if not k.startswith('__') and not callable(v)}
                print(f"   {class_attrs}")
        
        print("\n" + "=" * 60)
        print(f"✅ 完成打印 {len(dataclass_classes)} 个配置类")
        
    except ImportError as e:
        print(f"❌ 无法导入模块 {module_path}: {e}")
    except Exception as e:
        print(f"❌ 处理模块时发生错误: {e}")


def find_dataclass_subclasses(module: Any) -> Dict[str, type]:
    """
    在指定模块中查找所有 DataClassBase 的子类
    
    Args:
        module: 已导入的模块对象
        
    Returns:
        字典，键为类名，值为类对象
    """
    dataclass_classes = {}
    
    # 遍历模块中的所有属性
    for name in dir(module):
        obj = getattr(module, name)
        
        # 检查是否为类，且是 DataClassBase 的子类（但不是 DataClassBase 本身）
        if (inspect.isclass(obj) and 
            issubclass(obj, DataClassBase) and 
            obj is not DataClassBase):
            dataclass_classes[name] = obj
    
    return dataclass_classes


def get_all_dataclass_configs(module_path: str) -> Dict[str, Dict]:
    """
    获取指定模块下所有 DataClassBase 子类的配置字典
    
    Args:
        module_path: 模块路径
        
    Returns:
        字典，键为类名，值为配置字典
    """
    try:
        target_module = importlib.import_module(module_path)
        dataclass_classes = find_dataclass_subclasses(target_module)
        
        configs = {}
        for class_name, class_obj in dataclass_classes.items():
            try:
                instance = class_obj()
                configs[class_name] = instance.get_dict()
            except Exception as e:
                configs[class_name] = f"Error creating instance: {e}"
        
        return configs
        
    except Exception as e:
        return {"error": str(e)}


def compare_dataclass_configs(module_path1: str, module_path2: str) -> None:
    """
    比较两个模块中 DataClassBase 配置类的差异
    
    Args:
        module_path1: 第一个模块路径（如默认配置）
        module_path2: 第二个模块路径（如用户配置）
    """
    print(f"🔍 比较配置差异:")
    print(f"📋 默认配置: {module_path1}")
    print(f"👤 用户配置: {module_path2}")
    print("=" * 60)
    
    configs1 = get_all_dataclass_configs(module_path1)
    configs2 = get_all_dataclass_configs(module_path2)
    
    # 找出共同的配置类
    common_classes = set(configs1.keys()) & set(configs2.keys())
    
    if not common_classes:
        print("⚠️  两个模块中没有相同的配置类")
        return
    
    for class_name in common_classes:
        print(f"\n📦 配置类: {class_name}")
        
        config1 = configs1[class_name]
        config2 = configs2[class_name]
        
        if isinstance(config1, dict) and isinstance(config2, dict):
            # 比较配置项差异
            all_keys = set(config1.keys()) | set(config2.keys())
            
            for key in sorted(all_keys):
                val1 = config1.get(key, "❌ 未设置")
                val2 = config2.get(key, "❌ 未设置")
                
                if val1 != val2:
                    print(f"  🔄 {key}:")
                    print(f"    默认: {val1}")
                    print(f"    用户: {val2}")
                else:
                    print(f"  ✅ {key}: {val1}")
        else:
            print(f"  ⚠️  配置获取异常:")
            print(f"    默认: {config1}")
            print(f"    用户: {config2}")


# 便捷别名
print_configs = print_dataclass_configs 