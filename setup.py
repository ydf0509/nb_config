from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nb-config",
    version="1.1",
    author="ydf",
    author_email="ydf0509@sohu.com",
    description="一个优雅的Python配置覆盖系统，让用户可以透明地覆盖第三方库的配置",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ydf0509/nb_config",
    project_urls={
        "Bug Tracker": "https://github.com/ydf0509/nb_config/issues",
        "Documentation": "https://github.com/ydf0509/nb_config/wiki",
        "Source Code": "https://github.com/ydf0509/nb_config",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[
        "nb-log",
    ],
    keywords="config configuration override third-party library settings nb",
    include_package_data=True,
    zip_safe=False,
) 