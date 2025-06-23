# nb_config


一个Python配置覆盖系统，基于继承机制让用户可以透明地覆盖第三方库的配置，无需修改第三方库的任何代码。万能通用覆盖三方包的配置的包。

这个包适合写三方库的用户，如果三方包需要使用者能方便自定义覆盖三方库中的配置，则可以使用这个包。         
例如三方库中总是导入 config_default.py的配置，有些小白一看到三方包中的这种写法，很手痒老是想着手动修改三方包下的配置文件源码。   
使用这个包，就能让小白安心的复制三方包配置文件源码到自己项目下，然后修改自己项目中的配置文件中需要修改的配置。
（改三方包下的配置文件不好，每次新环境安装三方包或者升级三方包，配置文件都会被重置成默认的，用户需要重新修改配置文件。）

这个包不适合用户用来管理自己普通项目中的配置，因为用户自己项目下的的配置文件用户随便改就完了，没有涉及到这种覆盖需求。    

这样做，是为了用户能简单粗暴复制三方包种的配置文件到自己项目下，然后用户修改自己项目中的配置文件中需要修改的配置。

这个包是是为了三方包开发者使用。


```python
from nb_config.import_user_config import UserConfigAutoImporter

# 自动import0导入用户配置 ，没导入成功就复制三方包配置文件到用户项目根目录 sys.path[1]下新建配置文件。
# 这个通常放在三方包里面运行，而不是一般用户亲自使用这个方法
UserConfigAutoImporter(user_config_module_path='config_user2',
                       default_config_module_path='tests.mock_sitepackage.config_default').auto_import_user_config()

import tests.mock_sitepackage.site_packge_fun1_mod
from tests.mock_sitepackage.site_packge_fun2_mod import site_packge_fun2

if __name__ == '__main__':
    
    tests.mock_sitepackage.site_packge_fun1_mod.site_packge_fun1()
    site_packge_fun2()

    """
    三方包内部虽然没有亲自导入使用用户自己的配置模块，但能自动使用用户自己的配置文件中设置的值。
    输出结果：
    tests.mock_sitepackage.config_default.ConfigKLS1.config_a:用户自己的a
    tests.mock_sitepackage.config_default.ConfigKLS1.config_b:用户自己的b
    tests.mock_sitepackage.config_default.ConfigKLS1.config_c:三方包默认的c
    """
```