from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='celio',
    version=version,
    description='celio CRM',
    author='indictrans',
    author_email='priya.s@indictranstech.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
