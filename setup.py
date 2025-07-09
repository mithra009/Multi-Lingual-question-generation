"""
Setup script for Multi-Lingual Question Generator.
"""
from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="multi-lingual-question-generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered multi-lingual question generation from PDF documents",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/Multi-Lingual-question-generation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.0.0",
        ],
        "production": [
            "gunicorn>=20.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "question-generator=app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*", "static/*"],
    },
    keywords="nlp, question-generation, multi-lingual, ai, education, pdf-processing",
    project_urls={
        "Bug Reports": "https://github.com/your-username/Multi-Lingual-question-generation/issues",
        "Source": "https://github.com/your-username/Multi-Lingual-question-generation",
        "Documentation": "https://github.com/your-username/Multi-Lingual-question-generation#readme",
    },
) 