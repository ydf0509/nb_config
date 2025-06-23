"""
nb_config 装饰器模块
提供透明的第三方库配置覆盖功能
"""

from functools import wraps
import importlib
import nb_log

logger = nb_log.get_logger(__name__)


def nb_config_class(overwrite_config_module: str):
    """
    配置覆盖装饰器
    
    通过装饰器的方式，将用户自定义的配置透明地注入到第三方库的配置类中。
    第三方库无需任何修改，自动使用用户的配置值。
    
    Args:
        overwrite_config_module: 要覆盖的目标配置模块路径，如 'third_party.config'
        
    Returns:
        装饰器函数
        
    Example:
        ```python
        # third_party_lib/config.py
        class DatabaseConfig:
            host = 'localhost'
            port = 5432
            
        # your_project/my_config.py  
        from nb_config import nb_config_class
        
        @nb_config_class('third_party_lib.config')
        class DatabaseConfig:
            host = 'production-db.com'
            # port 保持默认值 5432
        ```
    """
    def _nbconfig(cls: type):
        # 首先检查是否是自己替换自己（在任何导入和处理之前）
        # 检查当前类是否就是要替换的目标类
        current_module = cls.__module__
        if current_module.endswith(overwrite_config_module):
            # print(f"🔄 检测到自引用，跳过配置覆盖: {cls.__name__} (自己替换自己)")
            return cls
            
        try:
            # 导入目标模块并获取同名配置类
            target_module = importlib.import_module(overwrite_config_module)
            target_config_class = getattr(target_module, cls.__name__)
            
            # 将用户配置类的属性注入到目标配置类中
            for key, value in cls.__dict__.items():
                if not key.startswith('__'):  # 跳过私有属性
                    logger.debug(f"配置覆盖: {target_config_class.__module__}.{target_config_class.__name__}.{key} = {value}")
                    setattr(target_config_class, key, value)
                    
            return cls  # 直接返回原类，保持用户代码不变
            
        except (ImportError, AttributeError) as e:
            logger.error(f"配置覆盖失败: {e}")
            # 如果目标模块或类不存在，仍然返回原类，避免中断用户程序
            return cls
            
    return _nbconfig 