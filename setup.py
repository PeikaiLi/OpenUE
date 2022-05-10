# -*- coding: utf-8 -*-


import os
import setuptools
# setup.py定义了打包程序的一些相关信息


with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()


# print(__file__ == os.path.realpath(__file__)) True 
# print(__file__)
# os.path.realpath() 输入一个文件的真实目录
# os.path.dirname() 取到文件夹

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="openue",  # 应用名
    version="0.2.5", # 版本号
    author="zxlzr",  # 作者
    author_email="jack16900@gmail.com", # 作者邮箱
    description="An open toolkit of universal extraction from text.", # 描述
    long_description=long_description, # 长文描述
    long_description_content_type="text/markdown", # 长文描述的文本格式
    url="https://github.com/zjunlp/openue", # 项目主页
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"), # 递归的打包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # 包的分类信息，见https://pypi.org/pypi?%3Aaction=list_classifiers
    install_requires=install_requires,# 自动安装依赖
    python_requires='>=3.6'
)
