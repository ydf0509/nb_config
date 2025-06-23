"""
演示 nb_config DataClassBase 的基本功能
"""

from nb_config import DataClassBase


def demo_basic_dataclass():
    """演示 DataClassBase 的基本功能"""
    print("🎯 演示：DataClassBase 基本功能")
    print("=" * 70)
    
    # 创建一个包含各种配置的示例
    class TestConfig(DataClassBase):
        database_url = "postgresql://user:password123@localhost:5432/mydb"
        redis_password = "secret_redis_pass"
        api_key = "abc123def456"
        debug = True
        port = 5432
        timeout = 30
        
    config = TestConfig()
    
    print("📋 配置字典输出:")
    print(config.get_dict())
    
    print("\n📋 普通JSON输出（可能泄露密码）:")
    print(config.get_json())
    
    print("\n🔒 加密JSON输出（密码已加密）:")
    print(config.get_pwd_enc_json())


def demo_inheritance():
    """演示基于继承的配置覆盖"""
    print("\n\n🔄 演示：基于继承的配置覆盖")
    print("=" * 70)
    
    # 模拟第三方库的默认配置
    class DefaultConfig(DataClassBase):
        host = 'localhost'
        port = 5432
        username = 'default_user'
        password = 'default_pass'
        database = 'default_db'
        debug = False
        
    print("📋 第三方库默认配置:")
    default_config = DefaultConfig()
    print(default_config.get_pwd_enc_json())
    
    # 用户的自定义配置（继承并覆盖）
    class UserConfig(DefaultConfig):
        host = 'production-db.com'
        username = 'prod_user'
        password = 'secure_password'
        debug = True
        # port, database 保持默认值
        
    print("\n👤 用户自定义配置（继承并覆盖部分属性）:")
    user_config = UserConfig()
    print(user_config.get_pwd_enc_json())
    
    print("\n🔍 对比差异:")
    print(f"  host: {default_config.host} -> {user_config.host}")
    print(f"  username: {default_config.username} -> {user_config.username}")
    print(f"  debug: {default_config.debug} -> {user_config.debug}")
    print(f"  port: {default_config.port} (继承，未修改)")
    print(f"  database: {default_config.database} (继承，未修改)")


def demo_real_world_usage():
    """演示真实世界的使用场景"""
    print("\n\n🌍 演示：真实世界使用场景")
    print("=" * 70)
    
    # 模拟从第三方库导入配置类
    print("📚 步骤1: 从第三方库导入配置类")
    
    class ThirdPartyDatabaseConfig(DataClassBase):
        """模拟第三方库的数据库配置"""
        host = 'localhost'
        port = 5432
        username = 'app'
        password = 'secret'
        database = 'app_db'
        pool_size = 10
        
    print("  第三方库配置已导入")
    
    # 创建用户自定义配置
    print("\n👤 步骤2: 创建用户自定义配置（继承第三方配置）")
    
    class DatabaseConfig(ThirdPartyDatabaseConfig):
        """用户的数据库配置，继承并覆盖第三方配置"""
        host = 'prod-db.example.com'
        username = 'prod_user'
        password = 'ultra_secure_password'
        pool_size = 20
        # port, database 保持第三方库的默认值
        
    print("  用户配置类已创建")
    
    # 模拟配置注入过程
    print("\n🔄 步骤3: 将用户配置注入到第三方库模块中")
    print("  (在实际使用中，这里会是: third_party_module.DatabaseConfig = DatabaseConfig)")
    
    # 展示最终效果
    print("\n🎯 步骤4: 配置覆盖效果")
    
    original_config = ThirdPartyDatabaseConfig()
    new_config = DatabaseConfig()
    
    print("📋 原始第三方配置:")
    print(original_config.get_pwd_enc_json(indent=2))
    
    print("\n👤 用户覆盖后的配置:")
    print(new_config.get_pwd_enc_json(indent=2))


if __name__ == '__main__':
    print("🎯 nb_config DataClassBase 功能演示")
    print("=" * 70)
    
    try:
        demo_basic_dataclass()
        demo_inheritance()
        demo_real_world_usage()
        
        print("\n" + "🎉" * 70)
        print("✅ 演示完成！")
        print("\n💡 关键要点:")
        print("  1. DataClassBase 提供配置管理和序列化功能")
        print("  2. 通过继承机制覆盖第三方库配置")
        print("  3. get_pwd_enc_json() 自动加密密码等敏感信息")
        print("  4. 只需覆盖需要修改的配置项，其余继承默认值")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc() 