from setuptools import setup, find_packages

setup(
    name="skill-matrix-manager",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.11",
        "python-json-logger>=3.2.1",
        "pytest>=8.3.4",
        "pytest-cov>=6.0.0",
        "mypy>=1.15.0",
        "psutil>=6.1.1",
    ],
    author="GingaDza",
    author_email="gingadza@example.com",
    description="スキルマトリックス管理アプリケーション",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
)
