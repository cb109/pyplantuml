# :coding: utf-8

import setuptools


setuptools.setup(
    name="pyplantuml",
    version="0.1.0",
    description="Creates UML diagrams from python source code.",
    long_description=open("README.rst").read(),
    keywords="uml, code analysis, overview, quickstart, diagram, OOP",
    url="https://cb109@bitbucket.org/cb109/pyplantuml.git",
    author="Christoph Buelter",
    author_email="c.buelter@arcor.de",
    packages=setuptools.find_packages(),
    install_requires=[
        "pylint"
    ],
    entry_points={
        "console_scripts": [
            "pyplantuml=pyplantuml.cli:main",
        ],
    }
)

