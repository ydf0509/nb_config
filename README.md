# nb_config

[![PyPI version](https://badge.fury.io/py/nb-config.svg)](https://badge.fury.io/py/nb-config)
[![Python versions](https://img.shields.io/pypi/pyversions/nb-config.svg)](https://pypi.org/project/nb-config/)
[![License](https://img.shields.io/github/license/ydf0509/nb_config.svg)](https://github.com/ydf0509/nb_config/blob/main/LICENSE)

一个优雅的Python配置覆盖系统，让用户可以透明地覆盖第三方库的配置，无需修改第三方库的任何代码。万能通用覆盖三方包的配置的包。

这个包适合写三方库的用户，如果三方包需要使用者能方便自定义覆盖三方库中的配置，则可以使用这个包。      
不适合用户用来管理自己普通项目中的配置，因为用户自己的配置自己直接写在配置文件中就完了，没有涉及到这种覆盖需求。

这样做，是为了用户能简单粗暴复制三方包种的配置文件到自己项目下，然后用户修改自己项目中的配置文件中需要修改的配置。

## ✨ 特性

- 🎯 **透明覆盖**: 第三方库无需任何修改，自动使用用户自定义配置
- 🛡️ **安全可靠**: 内置循环引用检测，防止自引用错误
- 🎨 **简洁优雅**: 仅需一个装饰器，20行核心代码解决复杂配置问题
- 📦 **部分覆盖**: 支持只覆盖需要修改的配置项，其余保持默认值
- 🔧 **即插即用**: 零依赖（除了日志），安装即用

## 🚀 快速开始

### 安装

```bash
pip install nb-config
```

### 基本用法

假设你正在使用一个第三方库，它有如下配置：

```python
# third_party_lib/config.py
class DatabaseConfig:
    host = 'localhost'
    port = 5432
    username = 'default_user'
    password = 'default_pass'
    database = 'default_db'
```

现在你想使用自己的数据库配置，传统方法需要修改第三方库代码或使用环境变量。使用 `nb_config`，你只需：

```python
# your_project/my_config.py
from nb_config import nb_config_class

@nb_config_class('third_party_lib.config')
class DatabaseConfig:
    host = 'your-production-db.com'
    username = 'your_user'
    password = 'your_secure_password'
    # 注意：我们没有设置 port 和 database，它们将保持第三方库的默认值
```

```python
# your_project/main.py
import your_project.my_config  # 导入你的配置（关键步骤！）
from third_party_lib import some_function

# 现在 third_party_lib 中的所有函数都会自动使用你的配置
some_function()  # 自动使用 your-production-db.com 而不是 localhost
```

就是这么简单！第三方库无需任何修改，自动使用你的配置。

## 📖 详细教程

### 工作原理

`nb_config` 的核心思想是"配置注入"：

1. 用户定义配置类并使用 `@nb_config_class` 装饰器
2. 装饰器在导入时自动将用户配置注入到第三方库的配置类中
3. 第三方库继续使用原有的配置访问方式，但得到的是用户自定义的值

### 实际应用场景

#### 场景1：Celery 配置覆盖

Celery 有200+个配置项，使用环境变量管理非常麻烦：

```python
# your_project/celery_config.py
from nb_config import nb_config_class

@nb_config_class('celery.app.defaults')
class Celery:
    broker_url = 'redis://your-redis:6379/0'
    result_backend = 'redis://your-redis:6379/1'
    task_serializer = 'json'
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'Asia/Shanghai'
    # 只需要配置你关心的选项，其余200+配置保持默认
```

```python
# your_project/tasks.py
import your_project.celery_config  # 导入配置
from celery import Celery

app = Celery('your_app')  # 自动使用你的配置
```

#### 场景2：数据库连接配置

```python
# your_project/db_config.py
from nb_config import nb_config_class

@nb_config_class('some_orm.config')
class DBConfig:
    DATABASE_URL = 'postgresql://user:pass@localhost/your_db'
    POOL_SIZE = 20
    MAX_OVERFLOW = 30
    # 其他配置保持默认
```

#### 场景3：日志配置覆盖

```python
# your_project/log_config.py
from nb_config import nb_config_class

@nb_config_class('third_party_lib.logging_config')
class LogConfig:
    level = 'INFO'
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    handlers = ['console', 'file']
```

### 高级用法

#### 1. 多层配置覆盖

```python
# base_config.py
from nb_config import nb_config_class

@nb_config_class('app.config')
class Config:
    debug = False
    secret_key = 'production-secret'

# development_config.py  
from nb_config import nb_config_class

@nb_config_class('app.config')
class Config:
    debug = True  # 开发环境覆盖
    # secret_key 保持 base_config 中的设置
```

#### 2. 条件配置覆盖

```python
import os
from nb_config import nb_config_class

@nb_config_class('app.config')
class Config:
    if os.getenv('ENVIRONMENT') == 'production':
        database_url = 'postgresql://prod-server/db'
    else:
        database_url = 'sqlite:///dev.db'
```

#### 3. 配置继承

```python
from nb_config import nb_config_class

class BaseConfig:
    timeout = 30
    retry_count = 3

@nb_config_class('third_party.config')
class MyConfig(BaseConfig):
    timeout = 60  # 覆盖基类配置
    # retry_count 继承基类的值
    custom_option = 'my_value'  # 新增配置
```

## 🔧 API 参考

### `@nb_config_class(module_path)`

**参数:**
- `module_path` (str): 要覆盖的目标配置模块路径

**返回:**
- 装饰器函数，返回原始类（不修改用户类）

**工作流程:**
1. 检查是否存在循环引用（自己覆盖自己）
2. 动态导入目标模块
3. 获取同名配置类
4. 将用户类的属性注入到目标类中
5. 返回用户类（保持不变）

**安全特性:**
- ✅ 自动检测循环引用
- ✅ 只覆盖非私有属性（不以`__`开头）
- ✅ 保持原有类结构不变
- ✅ 导入失败时优雅处理

## ⚠️ 注意事项

### 1. 导入顺序很重要

```python
# ✅ 正确：先导入配置，再使用第三方库
import your_config
from third_party import some_function

# ❌ 错误：第三方库已经加载了默认配置
from third_party import some_function
import your_config  # 太晚了，配置不会生效
```

### 2. 类名必须匹配

```python
# third_party/config.py
class DatabaseConfig:  # 第三方库的类名
    pass

# your_config.py
@nb_config_class('third_party.config')
class DatabaseConfig:  # 必须使用相同的类名
    pass
```

### 3. 避免循环引用

```python
# ❌ 错误：不要让配置类覆盖自己
@nb_config_class('your_module.config')  # 指向自己的模块
class Config:
    pass

# ✅ 正确：nb_config 会自动检测并跳过自引用
```

## 🧪 测试

```bash
# 克隆项目
git clone https://github.com/ydf0509/nb_config.git
cd nb_config

# 运行测试
python tests/mock_user_project/test_start_run.py
```

预期输出：
```
ConfigKLS1.config_a:用户自己的a
ConfigKLS1.config_b:用户自己的b  
ConfigKLS1.config_c:三方包默认的c
```

## 🤝 贡献

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md)。

### 开发设置

```bash
git clone https://github.com/ydf0509/nb_config.git
cd nb_config
pip install -e .
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关项目

- [nb_log](https://github.com/ydf0509/nb_log) - 强大的 Python 日志框架
- [funboost](https://github.com/ydf0509/funboost) - 分布式函数调度框架
- [distributed_framework](https://github.com/ydf0509/distributed_framework) - 分布式任务框架

## 💬 支持

- 🐛 [报告 Bug](https://github.com/ydf0509/nb_config/issues)
- 💡 [功能请求](https://github.com/ydf0509/nb_config/issues)
- 📖 [文档](https://github.com/ydf0509/nb_config/wiki)

---

**为什么选择 nb_config？**

传统的配置管理方案往往需要修改第三方库代码、使用复杂的环境变量或配置文件。`nb_config` 提供了一种更优雅的解决方案：**零侵入式配置覆盖**。

仅用一个装饰器和20行核心代码，就能让任何第三方库透明地使用你的自定义配置。这就是 `nb_config` 的魅力所在。 