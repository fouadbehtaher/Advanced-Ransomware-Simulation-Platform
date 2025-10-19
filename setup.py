"""
Setup script for Advanced Ransomware Simulation Platform (ARSP)
"""
from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="arsp",
    version="0.1.0",
    author="ARSP Development Team",
    description="Advanced Ransomware Simulation Platform for security testing and training",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fouadbehtaher/Advanced-Ransomware-Simulation-Platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "arsp=arsp.cli:main",
            "arsp-simulate=arsp.cli:simulate",
            "arsp-analyze=arsp.cli:analyze",
            "arsp-report=arsp.cli:report",
        ],
    },
    include_package_data=True,
)
