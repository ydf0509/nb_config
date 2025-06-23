
"""
这个文件是三方包的函数文件，里面是使用三方包默认配置文件的配置模块，但能自动使用用户自己的配置文件中设置的值。
"""
from  tests.mock_sitepackage.config_defualt import ConfigKLS1

def site_packge_fun2():
    """
    三方包的函数，里面是使用三方包默认配置文件的配置，但能自动使用用户自己的配置文件中设置的值。
    """
    print(f"ConfigKLS1.config_a:{ConfigKLS1.config_a}")
    print(f"ConfigKLS1.config_b:{ConfigKLS1.config_b}")
    print(f"ConfigKLS1.config_c:{ConfigKLS1.config_c}")





