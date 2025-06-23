
"""
这个文件模拟 三方包里面的配置文件，三方包里面其他地方始终导入使用的是这个模块的配置文件
"""

from nb_config import nb_config_class


'''
三方包的默认配置文件。

技术上这里不需要写@nb_config_class装饰器，但加上它有两个好处：
1. 验证自引用安全性：确保自己覆盖自己不会因循环引用而报错
2. 用户便利性：用户可以直接复制此文件作为配置模板，无需手动添加装饰器
'''
@nb_config_class('tests.mock_sitepackage.config_defualt') 
class ConfigKLS1:
    config_a = '三方包默认的a'
    config_b = '三方包默认的b'
    config_c = '三方包默认的c'