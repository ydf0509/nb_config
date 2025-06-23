
"""
nb_config 发布脚本
使用现代化的 build 工具发布到 PyPI
"""

import os
import sys
import subprocess
import shutil

def run_command(cmd, check=True):
    """运行命令并打印输出"""
    print(f"🔄 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0

def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        if '*' in dir_pattern:
            import glob
            for path in glob.glob(dir_pattern):
                if os.path.exists(path):
                    shutil.rmtree(path)
                    print(f"   删除: {path}")
        else:
            if os.path.exists(dir_pattern):
                shutil.rmtree(dir_pattern)
                print(f"   删除: {dir_pattern}")

def install_build_deps():
    """安装构建依赖"""
    print("📦 安装构建依赖...")
    return run_command("pip install --upgrade build twine")

def build_package():
    """构建包"""
    print("🔨 构建包...")
    return run_command("python -m build")

def upload_to_pypi():
    """上传到PyPI"""
    print("🚀 上传到 PyPI...")
    print("请输入PyPI用户名和密码，或确保已配置 ~/.pypirc")
    return run_command("python -m twine upload dist/*")

def main():
    """主函数"""
    print("🎯 nb_config 发布工具")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists('pyproject.toml'):
        print("❌ 错误：请在项目根目录运行此脚本")
        sys.exit(1)
    
    try:
        # 1. 清理
        clean_build()
        
        # 2. 安装依赖
        if not install_build_deps():
            print("❌ 安装构建依赖失败")
            sys.exit(1)
        
        # 3. 构建
        if not build_package():
            print("❌ 构建失败")
            sys.exit(1)
        
        # 4. 询问是否上传
        upload = input("\n✅ 构建成功！是否上传到 PyPI? (y/N): ").lower().strip()
        if upload in ['y', 'yes']:
            if upload_to_pypi():
                print("🎉 发布成功！")
                print("📦 查看包: https://pypi.org/project/nb-config/")
            else:
                print("❌ 上传失败")
                sys.exit(1)
        else:
            print("⏸️  构建完成，未上传。可以在 dist/ 目录查看构建结果")
            
    except KeyboardInterrupt:
        print("\n⏹️  用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 