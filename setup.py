# :coding: utf-8

import setuptools


setuptools.setup(
    name="pyplantuml",
    version="0.1.51",
    description="Creates UML diagrams from python source code.",
    long_description=open("README.md").read(),
    keywords="uml, code analysis, overview, quickstart, diagram, OOP",
    url="https://github.com/cb109/pyplantuml.git",
    author="Christoph Buelter",
    author_email="buelter.christoph@gmail.com",
    packages=setuptools.find_packages(),
    install_requires=[
        "astroid==1.3.2",
        "pylint==1.4"
    ],
    entry_points={
        "console_scripts": [
            "pyplantuml=pyplantuml.cli:convert_local",
            "pyplantuml-web=pyplantuml.cli:convert_online",
        ],
    }
)

