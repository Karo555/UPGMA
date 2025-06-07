from setuptools import setup

setup(
    name="UPGMA",
    version="0.1.0",
    packages=[
        "UPGMA",
        "NW.needleman_wunsch", 
        "MSA.multiple_sequence_alignment",
    ],
    package_dir={
        "UPGMA": "UPGMA/src",
        "NW.needleman_wunsch": "NW/needleman_wunsch",
        "MSA.multiple_sequence_alignment": "MSA/multiple_sequence_alignment",
    },
    install_requires=[
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "UPGMA = UPGMA.cli:main",
        ],
    },
)