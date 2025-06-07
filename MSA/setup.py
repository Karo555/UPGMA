from setuptools import setup, find_packages

setup(
    name="multiple_sequence_alignment",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
