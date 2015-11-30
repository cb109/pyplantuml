"""TODO

we have support for scanning a folder for modules now and analyzing
them in a single model: how to add support for any modules and packages?

why can some modules not be read by pclbr?

how to get the fields of a class and global variables of a module?

module namespaces (optional)?

add commandline interface (target, output, style, verbosity)

make it a pypi package

"""

import os
import sys
import pydoc
import pyclbr
import inspect
import pkgutil

from collections import defaultdict

import templates
# from py2plantuml import templates


def getClasses(moduleName):
    classes = pyclbr.readmodule(moduleName)
    return classes


def getFunctions(module):
    members = inspect.getmembers(module)
    functions = [m for m in members if inspect.isfunction(m)]
    return functions


def getModuleNamesFromFolder(folder, pkgpath='', done=None):
    """Write out HTML documentation for all modules in a directory tree."""
    modules = []
    if done is None: done = {}
    for importer, modname, ispkg in pkgutil.walk_packages([folder], pkgpath):
        modules.append(modname)
    return modules


def resolveModule(moduleName, forceload=0):
    obj = pydoc.locate(moduleName, forceload)
    if not obj:
        print ("Could not resolve module ", moduleName)
    return obj


class PlantUmlWriter(object):

    def __init__(self, model):
        self.model = model

        self.stream = ""

    def write(self, outputFile=None, title=None):
        self.stream += templates.STARTUML

        if title:
            titleLine = templates.TITLE.format(name=title)
            self.stream += titleLine

        styleLine = templates.STYLE
        self.stream += styleLine

        for moduleName, classes in self.model["moduleToClasses"].items():

            for className, classDescriptor in classes.items():
                self.stream += templates.EMPTY

                methods = sorted(classDescriptor.methods.keys())
                methodLines = ""
                for method in methods:
                    methodLines += templates.METHOD.format(
                        returnValue="", name=method
                    )
                # self.stream.write(
                    # templates.CLASS.format(
                    #     name=className, methods=methodLines
                    # )
                # )
                self.stream += "class " + className + "{\n"
                for methodLine in methodLines:
                    self.stream += methodLine
                self.stream += "}\n"

                supers = classDescriptor.super
                for super_ in supers:
                    if isinstance(super_, pyclbr.Class):
                        superName = super_.name
                    else:
                        superName = super_
                    if "mixin" in superName.lower():
                        relation = templates.COMPOSITION.format(
                            child=className, parent=superName
                        )
                    else:
                        relation = templates.INHERITANCE.format(
                            child=className, parent=superName
                        )
                    self.stream += relation

        self.stream += templates.ENDUML

        output = self.stream
        print (self.stream)
        if outputFile:
            with open(outputFile, "w") as f:
                f.write(output)
            print("Written to " + outputFile)
            os.system("plantuml " + outputFile)
            os.system(outputFile.replace(".txt", ".png"))
        else:
            print(output)


if __name__ == "__main__":

    moduleToClasses = defaultdict(dict)
    moduleToFunctions = defaultdict(list)

    args = sys.argv[1:]
    root = args[0]

    if "/" in root or "\\" in root or root in (".", ".."):
        # It's a directory path.
        sys.path.insert(0, root)
    else:
        # It's probably a module or package.
        print ("not supported atm")

    moduleNames = getModuleNamesFromFolder(root)

    outputFile = "plantuml.txt"

    for moduleName in moduleNames:
        classes = getClasses(moduleName)
        module = resolveModule(moduleName)
        functions = getFunctions(module)

        moduleToFunctions[moduleName].append(functions)
        moduleToClasses[moduleName].update(classes)

    model = {
        "moduleToFunctions": dict(moduleToFunctions),
        "moduleToClasses": dict(moduleToClasses),
    }

    PlantUmlWriter(model).write(outputFile)


# python inspecttest.py "c:\python34\lib\logging"