

from functools import wraps
import importlib
import nb_log

logger = nb_log.get_logger(__name__)


def nb_config_class(overwrite_config_module:str):
    def _nbconfig(cls:type):
        # 首先检查是否是自己替换自己（在任何导入和处理之前）
        # 检查当前类是否就是要替换的目标类
        current_module = cls.__module__
        if  current_module.endswith(overwrite_config_module):
            # print(f"🔄 检测到自引用，跳过配置覆盖: {cls.__name__} (自己替换自己)")
            return cls
        config_class = getattr(importlib.import_module(overwrite_config_module),cls.__name__)
        for key, value in cls.__dict__.items():
            if not key.startswith('__'):
                # logger.info(f"从 {cls.__module__} {cls.__name__} 设置  {config_class.__module__}.{config_class.__name__}.{key} = {value}")
                setattr(config_class, key, value)
        return cls  # 直接返回原类
    return _nbconfig




  