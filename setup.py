from setuptools import setup, find_packages

setup(
    name="creqit-bench",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=7.0",
        "gitpython~=3.1.30",
        "honcho",
        "jinja2~=3.1.3",
        "python-crontab~=2.6.0",
        "requests",
        "semantic-version~=2.10.0",
        "setuptools>=71.0.0",
    ],
    entry_points={
        "console_scripts": [
            "bench=creqit_bench.cli:cli",
        ],
    },
) 