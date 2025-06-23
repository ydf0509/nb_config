"""
这个文件模拟 三方包里面的配置文件，三方包里面其他地方始终导入使用的是这个模块的配置文件
"""

from nb_config import DataClassBase

# 三方包的默认配置文件
class ConfigKLS1(DataClassBase):
    config_a = 'config_user2 的a'
    config_b = 'config_user2 的b'
 