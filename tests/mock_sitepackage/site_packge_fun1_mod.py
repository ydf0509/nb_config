
"""
这个文件是三方包的函数文件，里面是使用三方包默认配置文件的配置模块，但能自动使用用户自己的配置文件中设置的值。
"""
import tests.mock_sitepackage.config_defualt

def site_packge_fun1():
    """
    三方包的函数，里面是使用三方包默认配置文件的配置，但能自动使用用户自己的配置文件中设置的值。
    """
    print(f"tests.mock_sitepackage.config_defualt.ConfigKLS1.config_a:{tests.mock_sitepackage.config_defualt.ConfigKLS1.config_a}")
    print(f"tests.mock_sitepackage.config_defualt.ConfigKLS1.config_b:{tests.mock_sitepackage.config_defualt.ConfigKLS1.config_b}")
    print(f"tests.mock_sitepackage.config_defualt.ConfigKLS1.config_c:{tests.mock_sitepackage.config_defualt.ConfigKLS1.config_c}")





