
"""
这个文件是用户测试文件的运行起点，测试三方包里面的函数是否能自动使用用户自己的配置文件中设置的值。
"""
import celery

print(f"celery.broker_url:{celery.broker_url}")


import tests.mock_user_project.config_user  # 这个是关键，用户只要导入了自己的模块，三方包里面自动使用用户自己的配置文件中设置的值。

import tests.mock_sitepackage.site_packge_fun1_mod
from tests.mock_sitepackage.site_packge_fun2_mod import site_packge_fun2

if __name__ == '__main__':
    
    tests.mock_sitepackage.site_packge_fun1_mod.site_packge_fun1()
    site_packge_fun2()

    """
    三方包内部虽然没有亲自导入使用用户自己的配置模块，单能自动使用用户自己的配置文件中设置的值。
    输出结果：
    tests.config_defualt.ConfigKLS1.config_a:用户自己的a
    tests.config_defualt.ConfigKLS1.config_b:用户自己的b
    tests.config_defualt.ConfigKLS1.config_c:三方包默认的c
    """


