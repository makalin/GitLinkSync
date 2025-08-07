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
    name="gitlinksync",
    version="1.0.0",
    author="Mehmet T. AKALIN",
    author_email="makalin@gmail.com",
    description="A tool to extract GitHub user links from X posts and automate follow-back actions",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/makalin/GitLinkSync",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "gitlinksync=src.cli:main_cli",
            "gitlinksync-dashboard=src.dashboard:app",
            "gitlinksync-scheduler=src.scheduler:schedule_jobs",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt"],
    },
    keywords="github, twitter, x, scraping, automation, follow-back, social-media",
    project_urls={
        "Bug Reports": "https://github.com/makalin/GitLinkSync/issues",
        "Source": "https://github.com/makalin/GitLinkSync",
        "Documentation": "https://github.com/makalin/GitLinkSync#readme",
    },
)
