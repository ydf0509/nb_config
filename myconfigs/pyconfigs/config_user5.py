"""
这个文件模拟 三方包里面的配置文件，三方包里面其他地方始终导入使用的是这个模块的配置文件
"""

from nb_config import DataClassBase

# 三方包的默认配置文件
class ConfigKLS1(DataClassBase):
    config_a = '用户自己的 config_user5 的 config_a'
  


class ConfigKLS222(DataClassBase):
    config_f = '用户自己的 config_user5 的 config_f'
    config_g = '用户自己的 config_user5 的 config_g'
    config_h = '用户自己的 config_user5 的 config_h'