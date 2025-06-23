
"""
这个文件模拟用户自己的配置文件，用户可以简单粗暴的复制三方包的默认配置文件，然后按需修改自己的配置文件，
三方包里面所有地方使用三方包默认配置文件的，自动使用用户自己的配置文件中设置的值。
"""
from nb_config import nb_config_class

@nb_config_class('tests.mock_sitepackage.config_default')
class ConfigKLS1:
    config_a = '用户自己的a' #用户的config_a覆盖三方包默认的config_a
    config_b = '用户自己的b' #用户的config_b覆盖三方包默认的config_b
    # config_c = '用户自己的c' #用户的config_c覆盖三方包默认的config_c ，可以不写，不写的话，就使用三方包默认的config_c





    
