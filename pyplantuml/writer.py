import os

from pylint.pyreverse.utils import is_interface

from pyplantuml import online


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
skinparam packageStyle frame
"""
OPEN = "{\n"
CLOSE = "}\n"
CLASS = "class {name} \n"
CLASSOPEN = "class {name} {{\n"
INTERFACE = "interface {name} \n"
INTERFACEOPEN = "interface {name} {{\n"
PACKAGE = "package {name} {{\n}}\n"
DEPENDS = "{parent} +-- {child}\n"
EXTENSION = "{parent} <|-- {child}\n"
COMPOSITION = "{parent} *-- {child}\n"
AGGREGATION = "{parent} o-- {child}\n"
CLASSMETHOD = "    {name}({args})\n"
CLASSATTR = "    {name}\n"

invokeplantuml = 'java -jar "{jar}" "{input}" -o "{output}"'
classes = "{package}_classes.txt"
packages = "{package}_packages.txt"

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


def getAttrBase(attr):
    """E.g. 'Filesystem : str' -> 'Filesystem' """
    return attr.split(":")[0].strip()


def getFieldTypePrefix(attr):
    """Magic fields are public."""
    if attr.startswith("__") and not attr.endswith("__"):
        return attr2type["private"]
    if attr.startswith("_") and not attr.endswith("__"):
        return attr2type["protected"]
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

    packagesFile = packages.format(package=diagram.title)
    with open(packagesFile, "w") as f:
        f.write(stream)
    return packagesFile


def writeClassDiagram(diagram):
    stream = STARTUML
    stream += STYLECLASS
    stream += TITLE.format(title=diagram.title)

    for obj in diagram.objects:
        attributes = diagram.get_attrs(obj.node)
        methods = diagram.get_methods(obj.node)

        if attributes or methods:
            template = INTERFACEOPEN if is_interface(obj.node) else CLASSOPEN
            stream += template.format(name=obj.title)

            for attr in sorted(attributes):
                attrDesc = getAttrDesc(attr)
                stream += CLASSATTR.format(name=attrDesc)

            for method in sorted(methods, key=lambda m: m.name):
                methodDesc = getAttrDesc(method.name)
                stream += CLASSMETHOD.format(
                    name=methodDesc, args=method.args.format_args()
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

    classesFile = classes.format(package=diagram.title)
    with open(classesFile, "w") as f:
        f.write(stream)
    return classesFile


def getLocalPlantUmlPath():
    """Returns the full path to plantuml.jar,
    if found on PATH, or None."""
    plantuml = "plantuml.jar"
    searchPaths = os.environ["PATH"].split(os.pathsep)
    for searchPath in searchPaths:
        plantumlPath = os.path.join(searchPath, plantuml)
        if os.path.isfile(plantumlPath):
            return os.path.abspath(plantumlPath)
    return None


def displayLocalImage(uml, jar):
    png = os.path.splitext(uml)[0] + ".png"
    cmd = invokeplantuml.format(jar=jar, input=uml, output=os.getcwd())
    os.system(cmd)
    os.system(png)
    return png


def displayOnline(uml, _):
    html = online.getResultFromPlantUmlServer(uml)
    url = online.displayInBrowser(html)
    return url


def toPlantUml(diadefs, plantumlArgs):
    umls = []
    try:
        packageDiagram, classDiagram = diadefs
        umls.append(writePackageDiagram(packageDiagram))
    except ValueError:
        classDiagram = diadefs[0]
    umls.append(writeClassDiagram(classDiagram))
    return umls


def visualize(umls):
    jar = getLocalPlantUmlPath()
    display = displayLocalImage if jar else displayOnline

    images = []
    for uml in umls:
        images.append(
            display(uml, jar)
        )
    return images