"""
演示如何打印指定模块下所有 DataClassBase 子类的 get_pwd_enc_json() 输出
"""

from nb_config import print_dataclass_configs, print_configs, compare_dataclass_configs


def demo_print_single_module():
    """演示打印单个模块的配置"""
    print("🎯 演示：打印单个模块的 DataClassBase 配置")
    print("=" * 70)
    
    # 打印第三方包的默认配置
    print("📋 第三方包默认配置:")
    print_dataclass_configs('tests.mock_sitepackage.config_default')
    
    print("\n" + "🔄" * 70)
    
    # 打印用户自定义配置  
    print("👤 用户自定义配置:")
    print_dataclass_configs('tests.mock_user_project.config_user')


def demo_compare_configs():
    """演示比较两个模块的配置差异"""
    print("\n\n🔍 演示：比较默认配置与用户配置的差异")
    print("=" * 70)
    
    compare_dataclass_configs(
        'tests.mock_sitepackage.config_default',      # 默认配置
        'tests.mock_user_project.config_user'         # 用户配置
    )


def demo_error_handling():
    """演示错误处理"""
    print("\n\n⚠️  演示：错误处理")
    print("=" * 70)
    
    # 尝试打印不存在的模块
    print("🔍 尝试打印不存在的模块:")
    print_dataclass_configs('non_existent_module')
    
    print("\n🔍 尝试打印没有 DataClassBase 子类的模块:")
    print_dataclass_configs('json')  # 标准库模块，没有DataClassBase子类


def demo_password_encryption():
    """演示密码加密功能"""
    print("\n\n🔒 演示：密码加密功能")
    print("=" * 70)
    
    # 创建一个包含密码的配置示例
    from nb_config import DataClassBase, nb_config_class
    
    class TestConfig(DataClassBase):
        database_url = "postgresql://user:password123@localhost:5432/mydb"
        redis_password = "secret_redis_pass"
        api_key = "abc123def456"
        debug = True
        port = 5432
    
    config = TestConfig()
    
    print("📋 普通JSON输出（可能泄露密码）:")
    print(config.get_json())
    
    print("\n🔒 加密JSON输出（密码已加密）:")
    print(config.get_pwd_enc_json())


if __name__ == '__main__':
    print("🎯 nb_config DataClassBase 配置打印功能演示")
    print("=" * 70)
    
    try:
        # 确保先导入配置文件，触发配置覆盖
        print("📚 导入配置文件以触发配置覆盖...")
        import tests.mock_user_project.config_user
        
        # 各种演示
        demo_print_single_module()
        demo_compare_configs()
        demo_error_handling()
        demo_password_encryption()
        
        print("\n" + "🎉" * 70)
        print("✅ 演示完成！")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc() 