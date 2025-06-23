import importlib
import inspect
import multiprocessing
from pathlib import Path
from shutil import copyfile
import sys

from nb_config.simple_data_class import DataClassBase

def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'

class UserConfigAutoImporter:
    """
    自动导入用户配置模块，如果用户配置模块不存在，则在 sys.path[1] 目录下自动创建一个用户配置模块。
    这个类通常由 三方框架内部去使用，而不是由用户亲自使用。
    """
    def __init__(self,user_config_module_path:str,default_config_module_path:str,
                 is_show_final_config:bool=True,
                 ):
        self.user_config_module_path=user_config_module_path # 用户配置模块的python import 路径
        self.default_config_module_path=default_config_module_path # 默认配置文件的python import路径
        self.is_show_final_config=is_show_final_config
        
    def auto_create_user_config_file(self):
        if '/lib/python' in sys.path[1] or r'\lib\python' in sys.path[1] or '.zip' in sys.path[1]:
            raise EnvironmentError(f'''如果是cmd 或者shell启动而不是pycharm 这种ide启动脚本，请先在会话窗口设置临时PYTHONPATH为你的项目路径，

                               windwos cmd 使用              set PYTHONNPATH=你的当前python项目根目录,
                               windows powershell 使用       $env:PYTHONPATH=你的当前python项目根目录,
                               linux 使用                    export PYTHONPATH=你的当前你python项目根目录,
                                   
                               PYTHONPATH 作用是python的基本常识，请ai问一下，不懂这个就太low了。
                               需要在会话窗口命令行设置临时的环境变量，而不是修改linux配置文件的方式设置永久环境变量，每个python项目的PYTHONPATH都要不一样，不要在配置文件写死
                               
                               懂PYTHONPATH 的重要性和妙用见： https://github.com/ydf0509/pythonpathdemo
                               ''')
        target_file_name = Path(sys.path[1]) / Path(f'{self.user_config_module_path}.py')
        source_file_name = importlib.import_module(self.default_config_module_path).__file__
        copyfile(source_file_name, target_file_name)
        print(f'在  {Path(sys.path[1])} 目录下自动生成了一个文件， 请刷新文件夹查看或修改 \n "{target_file_name}:1" 文件')
        

    def auto_import_user_config(self):
        """
        导入用户配置模块

        Args:
            module_path: 模块路径，如 'your_project.config'
            
        Returns:
            导入的模块对象
            
        Raises:
            ImportError: 当模块无法找到时，提供详细的解决方案
        """
        try:
            m= importlib.import_module(self.user_config_module_path)
            importlib.reload(m) 
            print(f'''import {self.user_config_module_path} 成功 ,使用 "{m.__file__}:1"  作为了配置文件''')
            dest_m = importlib.import_module(self.default_config_module_path)
            # importlib.reload(dest_m)
            if self.is_show_final_config:
                 for name in dir(dest_m):
                    config_cls = getattr(dest_m, name)
                    # 检查是否为类，且是 DataClassBase 的子类（但不是 DataClassBase 本身）
                    if (inspect.isclass(config_cls) and 
                        issubclass(config_cls, DataClassBase) and 
                        config_cls is not DataClassBase):
                        getattr(dest_m,name).update_cls_attribute(**getattr(m,name)().get_dict())
                        if self.is_show_final_config:
                            print(f'{name} 的最终融合配置: {config_cls().get_pwd_enc_json()}')
            
        except ModuleNotFoundError:
            self.auto_create_user_config_file()