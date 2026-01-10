"""Setup configuration for PE Assessment System"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="pe-assessment-system",
    version="0.1.0",
    author="PE Assessment Team",
    description="Automated marking and feedback system for GCSE PE assessments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hind450/pe-revision-checklist",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pypdf2>=3.0.0",
        "pdfplumber>=0.9.0",
        "PyMuPDF>=1.23.0",
        "python-docx>=0.8.11",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
        "ai": [
            "transformers>=4.30.0",
            "torch>=2.0.0",
            "sentence-transformers>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pe-assessment=src.main:main",
        ],
    },
)
