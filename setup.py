"""
Setup configuration for deep-diff.

This file is kept for backwards compatibility.
Modern Python packaging uses pyproject.toml instead.
For installation, use: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    packages=find_packages(),
)