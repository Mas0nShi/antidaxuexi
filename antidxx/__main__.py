# -*- coding:utf-8 -*-
"""
@Author: Mas0n
@File: __main__.py
@Time: 2022/5/28 21:06
@Desc: It's all about getting better.
"""
from antidxx import Version
from antidxx import generate

__version__ = Version




def main():
    print(generate(stdout=False))


if __name__ == '__main__':
    print(generate(stdout=False))
