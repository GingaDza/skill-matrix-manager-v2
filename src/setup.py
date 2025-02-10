"""
セットアップスクリプト
Created: 2025-02-09 13:10:33
Author: GingaDza
"""
from setuptools import setup, find_packages

setup(
    name="skill_matrix_manager",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
        "pandas>=1.0.0",
        "numpy>=1.19.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
    ],
)
