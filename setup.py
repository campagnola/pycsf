import os
from setuptools import setup, find_packages

root_pkg = 'pycsf'
packages = [root_pkg] + [root_pkg + '.' + sub_pkg for sub_pkg in find_packages(root_pkg)]

setup(
    name = root_pkg,
    version = "1.0",
    author = "Luke Campagnola",
    author_email = "lukec@alleninstitute.org",
    description = ("API and user interface for managing a database of experimental reagents, solutions, and recipes."),
    license = "Allen Institute Software License",
    keywords = "acsf solution reagent recipe editor",
    packages=packages,
    classifiers=[
    ],
)


