# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: setup.py
@Time: 2022/5/28 21:01
@Desc: It's all about getting better.
"""
import loguru
import setuptools
from antidxx import Version

loguru.logger.info(f"Package Version: {Version}")

setuptools.setup(
    name="antidxx",
    version=Version,
    description="fast to generate homeworks notices.",
    author="Mas0n",
    author_email="fishilir@gmail.com",
    url="https://github.com/Mas0nShi/antidaxuexi",
    install_requires=[
        "requests",
        "mloguru",
        "beautifulsoup4",
        "lxml"
    ],
    include_package_data=True,
    keywords="青春浙江 大学习 daxuexi qczj answers",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=setuptools.find_packages(where='.', exclude=(), include=('*',)),
    package_data={
        "antidxx.template": ["message.txt", "sections.txt", "staffs.txt"]
    },
    entry_points={
        'console_scripts': [
            "antidxx = antidxx.__main__:main",
        ]
    }
)