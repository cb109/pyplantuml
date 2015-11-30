import os
import sys

from astroid.inspector import Linker

from pylint.pyreverse.diadefslib import DiadefsHandler
from pylint.pyreverse.utils import is_interface
from pylint.pyreverse.main import Run


EMPTY = "\n"
STARTUML = "@startuml\n"
ENDUML = "@enduml\n"
TITLE = "title {title}\n"
STYLECLASS = """
skinparam class {
    BackgroundColor White
    ArrowColor Grey
    BorderColor Black
}

"""
STYLEPACKAGE = """
skinparam package {
    BackgroundColor White
    ArrowColor Grey
    BorderColor Black
}

"""
OPEN = "{\n"
CLOSE = "}\n"
CLASS = "class {name} \n"
CLASSOPEN = "class {name} {{\n"
INTERFACE = "interface {name} \n"
INTERFACEOPEN = "interface {name} {{\n"
PACKAGE = "package {name} \n"
DEPENDS = "{parent} +-- {child}\n"
EXTENSION = "{parent} <|-- {child}\n"
COMPOSITION = "{parent} *-- {child}\n"
AGGREGATION = "{parent} o-- {child}\n"
CLASSMETHOD = "    {name}({args})\n"
CLASSATTR = "    {name}\n"

relationship2plantuml = {
    "specialization" : EXTENSION,
    "association" : AGGREGATION,
    "implements" : COMPOSITION
}
attr2type = {
    "public" : "+",
    "protected" : "#",
    "private" : "-"
}


def getPublicAttrs(attributes):
    return filter(lambda a: not a.startswith("_"), attributes)


def getPrivateAttrs(attributes):
    return filter(lambda a: a.startswith("__"), attributes)


def getProtectedAttrs(attributes):
    return filter(lambda a: a.startswith("_") and not a.startswith("__"), attributes)


def getAttrBase(attr):
    """E.g. 'Filesystem : str' -> 'Filesystem' """
    return attr.split(":")[0].strip()


def getFieldTypePrefix(attr):
    if attr.startswith("__"): return attr2type["private"]
    if attr.startswith("_"): return attr2type["protected"]
    return attr2type["public"]


def getAttrDesc(attr):
    base = getAttrBase(attr)
    desc = getFieldTypePrefix(attr) + base
    return desc


def writePackageDiagram(diagram):
    stream = STARTUML
    stream += STYLEPACKAGE

    stream += TITLE.format(title=diagram.title)

    for module in diagram.modules():
        stream += PACKAGE.format(name=module.title)

    for relation_type, relationsships in diagram.relationships.items():
        for rel in relationsships:
            stream += DEPENDS.format(
                parent=rel.to_object.title, child=rel.from_object.title
            )
    stream += "\n" + ENDUML

    with open("packages.txt", "w") as f:
        f.write(stream)


def writeClassDiagram(diagram):
    stream = STARTUML
    stream += STYLECLASS

    stream += TITLE.format(title=diagram.title)

    # modules = []

    for obj in diagram.objects:
        # objModule = obj.node.root()
        # if objModule not in modules:
        #     modules.append(objModule)
        #     pprint (objModule.locals)


        attributes = diagram.get_attrs(obj.node)
        methods = diagram.get_methods(obj.node)
        if attributes or methods:
            template = INTERFACEOPEN if is_interface(obj.node) else CLASSOPEN
            stream += template.format(name=obj.title)

            # magics = getMagicAttrs()
            publics = getPublicAttrs(attributes)
            protecteds = getProtectedAttrs(attributes)
            privates = getPrivateAttrs(attributes)

            # if publics:
            #     stream += ".. public ..\n"
            for attr in sorted(publics):
                stream += getAttrDesc(attr) + "\n"

            # if protecteds:
            #     stream += ".. protected ..\n"
            for attr in sorted(protecteds):
                stream += getAttrDesc(attr) + "\n"

            # if privates:
            #     stream += ".. private ..\n"
            for attr in sorted(privates):
                stream += getAttrDesc(attr) + "\n"

            # for attr in sorted(attributes):
            #     shortAttr = attr.split(":")[0].strip()
            #     prefixedAttr = getFieldTypePrefix(shortAttr) + shortAttr
            #     stream += CLASSATTR.format(name=prefixedAttr)

            # stream += "==\n"

            for method in sorted(methods, key=lambda m: m.name):
                prefixedMethod = getFieldTypePrefix(method.name) + method.name
                stream += CLASSMETHOD.format(
                    name=prefixedMethod, args=method.args.format_args()
                )

            stream += CLOSE
        else:
            template = INTERFACE if is_interface(obj.node) else CLASS
            stream += template.format(name=obj.title)

    stream += EMPTY

    for relation_type, relationsships in diagram.relationships.items():
        for rel in relationsships:
            stream += relationship2plantuml[rel.type].format(
                parent=rel.to_object.title, child=rel.from_object.title
            )
    stream += "\n" + ENDUML

    with open("classes.txt", "w") as f:
        f.write(stream)


class CustomRun(Run):

    def run(self, args):
        """checking arguments and run project"""
        if not args:
            print(self.help())
            return 1
        # insert current working directory to the python path to recognize
        # dependencies to local modules even if cwd is not in the PYTHONPATH
        sys.path.insert(0, os.getcwd())
        try:
            project = self.manager.project_from_files(args)
            linker = Linker(project, tag=True)
            handler = DiadefsHandler(self.config)
            diadefs = handler.get_diadefs(project, linker)
        finally:
            sys.path.pop(0)

        # For some reason the diagram titles are
        #not set correctly, so fix that here if needed.
        title = args[-1]
        for diagram in diadefs:
            if "No Name" in diagram.title:
                diagram.title = title

        try:
            packageDiagram, classDiagram = diadefs
            writePackageDiagram(packageDiagram)
        except ValueError:
            classDiagram = diadefs[0]
        writeClassDiagram(classDiagram)


def main():
    args = sys.argv[1:]
    CustomRun(args)


if __name__ == "__main__":
    main()