# 发布说明

## 发布到 PyPI 的步骤

### 1. 准备工作

确保已安装必要的工具：
```bash
pip install build twine
```

### 2. 自动发布（推荐）

使用提供的发布脚本：
```bash
python publish.py
```

### 3. 手动发布

#### 3.1 构建包
```bash
# 清理旧文件
rm -rf build/ dist/ *.egg-info/

# 构建包
python -m build
```

#### 3.2 检查包
```bash
python -m twine check dist/*
```

#### 3.3 上传到测试 PyPI（可选）
```bash
python -m twine upload --repository testpypi dist/*
```

测试安装：
```bash
pip install -i https://test.pypi.org/simple/ nb-config
```

#### 3.4 上传到正式 PyPI
```bash
python -m twine upload dist/*
```

### 4. 验证安装

```bash
pip install nb-config
python -c "from nb_config import DataClassBase; print('✅ 安装成功')"
```

## 版本发布清单

- [ ] 更新版本号（setup.py 和 pyproject.toml）
- [ ] 更新 README.md
- [ ] 运行测试 `python tests/mock_user_project/test_start_run.py`
- [ ] 构建包 `python -m build`
- [ ] 检查包 `python -m twine check dist/*`
- [ ] 上传到测试 PyPI（可选）
- [ ] 上传到正式 PyPI
- [ ] 创建 GitHub Release
- [ ] 更新文档

## 注意事项

1. **PyPI 账号配置**：确保已配置 PyPI API token
   ```bash
   # 在 ~/.pypirc 中配置
   [pypi]
   username = __token__
   password = pypi-your-api-token
   ```

2. **版本管理**：每次发布前记得更新版本号

3. **依赖检查**：确保 `nb-log` 依赖版本正确

4. **文档同步**：GitHub README 和 PyPI 描述保持一致 