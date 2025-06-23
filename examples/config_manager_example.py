"""
nb_config ConfigManager 使用示例
展示如何用统一的配置管理器替代 nb_log、funboost 中的重复配置代码
"""

from nb_config import ConfigManager, auto_load_config


def example_funboost_style_config():
    """
    模拟 funboost 风格的配置管理
    替代原来 use_config_form_funboost_config_module() 函数
    """
    print("🚀 示例：funboost 风格的配置管理")
    
    # 创建配置管理器（替代原来的复杂逻辑）
    config_manager = ConfigManager(
        config_name='funboost_config',
        target_module='funboost.config_default',  # 假设的目标模块
        default_config_path='funboost/funboost_config_default.py',  # 模板路径
        auto_create=True,
        config_class_names=['BrokerConnConfig', 'FunboostCommonConfig']
    )
    
    try:
        # 自动查找、创建、导入配置文件
        config = config_manager.load_config()
        print(f"✅ funboost 配置加载成功: {config}")
        
    except Exception as e:
        print(f"❌ funboost 配置加载失败: {e}")


def example_nb_log_style_config():
    """
    模拟 nb_log 风格的配置管理
    """
    print("\n📋 示例：nb_log 风格的配置管理")
    
    # 使用便捷函数（一行代码搞定）
    try:
        config = auto_load_config(
            config_name='nb_log_config',
            target_module='nb_log.config_default',
            auto_create=True
        )
        print(f"✅ nb_log 配置加载成功: {config}")
        
    except Exception as e:
        print(f"❌ nb_log 配置加载失败: {e}")


def example_custom_project_config():
    """
    自定义项目的配置管理示例
    """
    print("\n🛠️ 示例：自定义项目配置管理")
    
    config_manager = ConfigManager(
        config_name='my_project_config',
        auto_create=True,
        search_paths=['./config', './settings', '.']  # 自定义搜索路径
    )
    
    try:
        config = config_manager.load_config()
        print(f"✅ 自定义项目配置加载成功: {config}")
        
        # 演示热重载
        print("🔄 演示配置热重载...")
        reloaded_config = config_manager.load_config(reload=True)
        print(f"✅ 配置重新加载成功: {reloaded_config}")
        
    except Exception as e:
        print(f"❌ 自定义项目配置加载失败: {e}")


def compare_before_after():
    """
    对比使用配置管理器前后的代码复杂度
    """
    print("\n📊 代码复杂度对比")
    
    print("""
=== 使用 ConfigManager 之前 ===
每个项目都要写的重复代码：

def use_config_from_xxx():
    # 50+ 行重复逻辑
    current_script_path = sys.path[0]
    project_root_path = sys.path[1]
    
    # 多层级查找
    for path in [current_script_path, project_root_path, ...]:
        if exists(path / 'xxx_config.py'):
            break
    
    # 环境检查
    if '/lib/python' in sys.path[1]:
        raise EnvironmentError("复杂的错误信息...")
    
    # 自动创建文件
    if not found:
        copyfile(template, target)
    
    # 动态导入和合并
    module = importlib.import_module('xxx_config')
    importlib.reload(module)
    merge_config(module)

=== 使用 ConfigManager 之后 ===
每个项目只需要：

config = auto_load_config('xxx_config', 'target.module')

# 或者稍微复杂的场景：
manager = ConfigManager('xxx_config', auto_create=True)
config = manager.load_config()

减少了 90% 的重复代码！
""")


if __name__ == '__main__':
    print("🎯 nb_config ConfigManager 示例演示")
    print("=" * 50)
    
    # 运行示例
    example_funboost_style_config()
    example_nb_log_style_config()
    example_custom_project_config()
    compare_before_after()
    
    print("\n🎉 示例演示完成！")
    print("💡 使用 ConfigManager 可以大大减少项目间的重复配置代码") 