"""
这个文件模拟用户自己的配置文件，用户可以简单粗暴的复制三方包的默认配置文件，然后按需修改自己的配置文件，
三方包里面所有地方使用三方包默认配置文件的，自动使用用户自己的配置文件中设置的值。
"""
from nb_config import DataClassBase


# 继承第三方包的配置类，覆盖需要修改的配置项
class ConfigKLS1(DataClassBase):
    config_a = 'tests.mock_user_project.config_user 的a'  # 用户的config_a覆盖三方包默认的config_a
    config_b = 'tests.mock_user_project.config_user 的b'  # 用户的config_b覆盖三方包默认的config_b
    # config_c = '用户自己的c'  # 可以不写，不写的话，就继承三方包默认的config_c






    
