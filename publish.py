# -*- coding: utf-8 -*-
"""
PyPI 发布脚本

使用方法:
1. 确保已安装必要工具: pip install twine build
2. 运行: python publish.py
"""

import os
import sys
import subprocess
import shutil


def run_command(cmd):
    """运行命令并打印输出"""
    print(f"🔧 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"❌ 命令执行失败: {cmd}")
        sys.exit(1)
    return result


def clean_build():
    """清理构建文件"""
    print("🧹 清理旧的构建文件...")
    dirs_to_clean = ['build', 'dist', 'nb_config.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除: {dir_name}")


def build_package():
    """构建包"""
    print("📦 构建包...")
    run_command("python -m build")


def check_package():
    """检查包的完整性"""
    print("🔍 检查包...")
    run_command("python -m twine check dist/*")


def upload_to_testpypi():
    """上传到测试PyPI"""
    print("🧪 上传到测试PyPI...")
    run_command("python -m twine upload --repository testpypi dist/*")


def upload_to_pypi():
    """上传到正式PyPI"""
    print("🚀 上传到正式PyPI...")
    run_command("python -m twine upload dist/*")


def main():
    print("🎯 nb_config PyPI 发布脚本")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists("nb_config/__init__.py"):
        print("❌ 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 清理构建文件
    clean_build()
    
    # 构建包
    build_package()
    
    # 检查包
    check_package()
    
    # 询问用户要上传到哪里
    print("\n选择发布目标:")
    print("1. TestPyPI (测试环境)")
    print("2. PyPI (正式环境)")
    print("3. 两者都发布")
    print("0. 仅构建，不上传")
    
    choice = input("\n请选择 (0-3): ").strip()
    
    if choice == "1":
        upload_to_testpypi()
        print("✅ 已上传到 TestPyPI")
        print("🔗 测试安装: pip install -i https://test.pypi.org/simple/ nb-config")
    elif choice == "2":
        upload_to_pypi()
        print("✅ 已上传到 PyPI")
        print("🔗 安装: pip install nb-config")
    elif choice == "3":
        upload_to_testpypi()
        print("✅ 已上传到 TestPyPI")
        
        confirm = input("\n是否继续上传到正式PyPI? (y/N): ").strip().lower()
        if confirm == 'y':
            upload_to_pypi()
            print("✅ 已上传到 PyPI")
            print("🔗 安装: pip install nb-config")
        else:
            print("⏹️  跳过正式PyPI上传")
    elif choice == "0":
        print("✅ 构建完成，包文件在 dist/ 目录中")
    else:
        print("❌ 无效选择")
        sys.exit(1)
    
    print("\n🎉 发布流程完成！")


if __name__ == "__main__":
    main() 