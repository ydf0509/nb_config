
"""
这个文件是用户测试文件的运行起点，测试三方包里面的函数是否能自动使用用户自己的配置文件中设置的值。
"""


from nb_config.import_user_config import UserConfigAutoImporter

UserConfigAutoImporter(user_config_module_path='config_user2',
                       default_config_module_path='tests.mock_sitepackage.config_default').auto_import_user_config()

import tests.mock_sitepackage.site_packge_fun1_mod
from tests.mock_sitepackage.site_packge_fun2_mod import site_packge_fun2

if __name__ == '__main__':
    
    tests.mock_sitepackage.site_packge_fun1_mod.site_packge_fun1()
    site_packge_fun2()

    """
    三方包内部虽然没有亲自导入使用用户自己的配置模块，单能自动使用用户自己的配置文件中设置的值。
    输出结果：
    tests.mock_sitepackage.config_default.ConfigKLS1.config_a:用户自己的a
    tests.mock_sitepackage.config_default.ConfigKLS1.config_b:用户自己的b
    tests.mock_sitepackage.config_default.ConfigKLS1.config_c:三方包默认的c
    """


