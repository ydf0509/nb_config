import importlib

def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'

class UserConfigAutoImporter:
    def __init__(self,user_config_module_path:str,default_config_module_path_file:str):
        self.user_config_module_path=user_config_module_path # 用户配置模块的python import 路径
        self.default_config_module_path_file=default_config_module_path_file # 默认配置文件的文件夹路径
        

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
            print(f'''import module_path sucess ，use "{m.__file__}:1"  as config file''')
            return m
        except ModuleNotFoundError:
            raise ImportError(f'''
❌ 无法导入用户配置模块: {self.user_config_module_path}

🔍 请检查以下几点:
1. 配置文件是否存在
2. 配置文件是否在 Python 路径中

💡 建议解决方案:
• 将配置文件放在项目根目录下（推荐）
【实际你可以放在你电脑磁盘的任意文件夹下，只要这个文件夹你添加到了pythonpath，就能被python找到；
但放在项目根目录下，是为了复用好处，即使你不用这个包，对任意项目，把当前项目的根目录添加到当前会话的临时环境变量的pythonpath也是有益无害】
• 项目根目录通常会自动添加到 Python 路径中
• 在 PyCharm 等 IDE 中，项目根目录会自动加入 Python 路径

🚀 如果在终端运行，请先设置 PYTHONPATH:

Linux/Mac:
export PYTHONPATH=/path/to/your/project

Windows CMD:
set PYTHONPATH=C:\\path\\to\\your\\project

Windows PowerShell:
$env:PYTHONPATH = "C:\\path\\to\\your\\project"

然后再运行你的 Python 脚本。

pythonpath 基本知识过于薄弱的，需要看 https://github.com/ydf0509/pythonpathdemo 这个项目，说明懂pythonpath的重要性。
                        '''
                        )
  
    





