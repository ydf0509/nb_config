"""
nb_config 配置管理使用示例
展示基于继承的配置覆盖机制
"""

from nb_config import DataClassBase


def example_basic_inheritance():
    """
    基本的继承配置覆盖示例
    """
    print("🚀 示例：基本的继承配置覆盖")
    print("=" * 70)
    
    # 模拟第三方库的默认配置
    class ThirdPartyConfig(DataClassBase):
        """第三方库的默认配置"""
        database_host = 'localhost'
        database_port = 5432
        debug = False
        max_connections = 10
        timeout = 30
        
    print("📋 第三方库默认配置:")
    default_config = ThirdPartyConfig()
    print(default_config.get_json(indent=2))
    
    # 用户的自定义配置（继承并覆盖）
    class UserConfig(ThirdPartyConfig):
        """用户自定义配置，继承并覆盖需要修改的项"""
        database_host = 'prod-server.example.com'
        debug = True
        max_connections = 50
        # database_port, timeout 保持默认值
        
    print("\n👤 用户自定义配置:")
    user_config = UserConfig()
    print(user_config.get_json(indent=2))
    
    print("\n✅ 继承配置覆盖演示完成")


def example_funboost_style_config():
    """
    模拟 funboost 风格的配置管理
    展示如何在真实项目中使用继承方式
    """
    print("\n\n🔧 示例：funboost 风格的配置管理")
    print("=" * 70)
    
    # 模拟 funboost 的默认配置类
    class FunboostDefaultConfig(DataClassBase):
        """模拟 funboost 的默认配置"""
        broker_kind = 'redis'
        redis_host = '127.0.0.1'
        redis_port = 6379
        redis_password = ''
        redis_db = 0
        
        queue_name = 'default_queue'
        max_workers = 4
        log_level = 'INFO'
        
    print("📋 funboost 默认配置:")
    default_config = FunboostDefaultConfig()
    print(default_config.get_pwd_enc_json(indent=2))
    
    # 用户的生产环境配置
    class ProductionConfig(FunboostDefaultConfig):
        """生产环境配置"""
        redis_host = 'prod-redis.example.com'
        redis_password = 'secure_redis_password'
        redis_db = 1
        
        queue_name = 'production_queue'
        max_workers = 16
        log_level = 'WARNING'
        
    print("\n🏭 生产环境配置:")
    prod_config = ProductionConfig()
    print(prod_config.get_pwd_enc_json(indent=2))
    
    # 模拟配置注入过程
    print("\n🔄 配置注入过程:")
    print("  import funboost.config_default")
    print("  funboost.config_default.BrokerConfig = ProductionConfig")
    print("  # 现在 funboost 所有地方都会使用生产环境配置")


def example_nb_log_style_config():
    """
    模拟 nb_log 风格的配置管理
    """
    print("\n\n📋 示例：nb_log 风格的配置管理")
    print("=" * 70)
    
    # 模拟 nb_log 的默认配置
    class NbLogDefaultConfig(DataClassBase):
        """模拟 nb_log 的默认配置"""
        log_level = 'DEBUG'
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        log_file = None
        max_file_size = 100 * 1024 * 1024  # 100MB
        backup_count = 5
        
    print("📋 nb_log 默认配置:")
    default_config = NbLogDefaultConfig()
    print(default_config.get_json(indent=2))
    
    # 用户的自定义日志配置
    class CustomLogConfig(NbLogDefaultConfig):
        """用户自定义日志配置"""
        log_level = 'INFO'
        log_file = 'app.log'
        max_file_size = 50 * 1024 * 1024  # 50MB
        backup_count = 10
        
    print("\n👤 用户自定义日志配置:")
    custom_config = CustomLogConfig()
    print(custom_config.get_json(indent=2))
    
    print("\n🔄 配置注入:")
    print("  import nb_log.config_default")
    print("  nb_log.config_default.LogConfig = CustomLogConfig")


def compare_before_after():
    """
    对比装饰器方式与继承方式的代码复杂度
    """
    print("\n\n📊 代码复杂度对比")
    print("=" * 70)
    
    print("""
=== 装饰器方式（旧方式） ===
from nb_config import nb_config_class, DataClassBase

@nb_config_class('third_party.config')
class DatabaseConfig(DataClassBase):
    host = 'prod-server.com'
    port = 5432

# 优点：语法简洁，自动注入
# 缺点：动态注入复杂，难以调试，循环引用风险

=== 继承方式（新方式） ===
from nb_config import DataClassBase
from third_party.config import DatabaseConfig as DefaultConfig

class DatabaseConfig(DefaultConfig):
    host = 'prod-server.com'
    # port 继承默认值

import third_party.config
third_party.config.DatabaseConfig = DatabaseConfig

# 优点：面向对象，清晰直观，易于调试，类型安全
# 缺点：需要手动注入（但这也提供了更多控制）
""")


def demonstrate_advanced_patterns():
    """
    演示高级使用模式
    """
    print("\n\n🚀 高级使用模式")
    print("=" * 70)
    
    # 多层继承配置
    class BaseConfig(DataClassBase):
        """基础配置"""
        app_name = 'my_app'
        debug = False
        
    class DatabaseConfig(BaseConfig):
        """数据库配置层"""
        host = 'localhost'
        port = 5432
        
    class ProductionConfig(DatabaseConfig):
        """生产环境配置（多层继承）"""
        debug = False
        host = 'prod-db.example.com'
        pool_size = 20
        
    print("🏗️ 多层继承配置:")
    prod_config = ProductionConfig()
    print(prod_config.get_json(indent=2))
    
    # 条件配置
    import os
    
    class ConditionalConfig(BaseConfig):
        """条件配置"""
        if os.getenv('ENV') == 'production':
            debug = False
            log_level = 'WARNING'
        else:
            debug = True
            log_level = 'DEBUG'
            
    print("\n🔀 条件配置:")
    conditional_config = ConditionalConfig()
    print(conditional_config.get_json(indent=2))


if __name__ == '__main__':
    print("🎯 nb_config 基于继承的配置管理演示")
    print("=" * 70)
    
    # 运行示例
    example_basic_inheritance()
    example_funboost_style_config()
    example_nb_log_style_config()
    compare_before_after()
    demonstrate_advanced_patterns()
    
    print("\n🎉 示例演示完成！")
    print("💡 使用继承方式可以提供更清晰、更安全的配置覆盖机制") 