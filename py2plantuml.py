import os
import sys
import pyclbr
import pkgutil
import setuptools

STARTUML = "@startuml\n"
ENDUML = "@enduml\n"
TITLE = "title {package}\n"
STYLE = """
skinparam class {
    BackgroundColor White
    ArrowColor Grey
    BorderColor Black
}

"""
INHERITANCE = "{parent} <|-- {child}\n"
COMPOSITION = "{parent} *-- {child}\n"
CLASSMETHOD = "{child} : {method}\n"


def getCodeFromFile(filePath):
    with open(filePath) as f:
        code = f.read()
        return code


def getCodeLinesFromFile(filePath):
    with open(filePath) as f:
        lines = f.readlines()
        return lines


def yieldModules(package):
    data = pkgutil.walk_packages(path=package, onerror=lambda m: None)
    for importer, module, isPackage in data:
        yield module


def getPackages(directory):
    packages = setuptools.find_packages(directory)
    return packages


def getRelationLine(parent, child):
    if "mixin" in parent.lower():
        return COMPOSITION.format(**locals())
    else:
        return INHERITANCE.format(**locals())


def getMethodLine(child, method):
    return CLASSMETHOD.format(**locals())


def toPlantUML(module, outputFile):
    if os.path.isfile(module):
        module = os.path.splitext(os.path.basename(module))[0]

    with open(outputFile, "w") as f:
        f.write(STARTUML)
        f.write(STYLE)
        title = TITLE.format(package=module)
        f.write(title)

        classDescriptors = pyclbr.readmodule(module)
        for className, classData in classDescriptors.items():
            child = className
            methods = sorted([m + "()" for m in classData.methods])
            parents = [p.name if hasattr(p, "name") else str(p) for p in classData.super]

            for parent in parents:
                relationLine = getRelationLine(parent, child)
                f.write(relationLine)

            for method in methods:
                methodLine = getMethodLine(child, method)
                f.write(methodLine)
        f.write(ENDUML)

    os.system("notepad " + outputFile)


if __name__ == "__main__":
    args = sys.argv[1:]
    module, outputFile = args
    toPlantUML(module, outputFile)