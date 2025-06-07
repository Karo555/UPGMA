from setuptools import setup, find_packages

setup(
    name="phylo_core",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib",  
    ],
    entry_points={
        "console_scripts": [
            "UPGMA = src.cli:main",
        ],
    },
)
