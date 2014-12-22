pyplantuml
==========

Creates UML diagrams from python source code.

Build on top of pylint's pyreverse to do the static code analysis
and supports most of its original commandline interface.


Installation
------------

    pip install pyplantuml


Dependencies
------------

    pylint, for it includes astroid and pyreverse.


Usage
-----

cd <parent-dir-of-package>
pyplantuml [pyreverse-options] -- [options] <package>