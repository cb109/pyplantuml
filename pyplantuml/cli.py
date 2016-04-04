import os
import sys

from pyplantuml import adapter
from pyplantuml import writer
from pyplantuml import online


def parseArgs(args):
    return args


def getTargetPackage(args):
    """Get package name from path."""
    target = args[-1]
    package = target
    if "/" in target or "\\" in target or target in (".", ".."):
        package = os.path.basename(target)
    return package


def fixDiagramTitle(diadefs, title):
    for i, diagram in enumerate(diadefs):
        if "No Name" in diagram.title:
            diadefs[i].title = title
    return diadefs


def main(convert_online=False):
    args = sys.argv[1:]
    if not args:
        print ("""
pyplantuml
----------

Usage:

    pyplantuml [pyreverse-options] <package>

        If a plantuml.jar can be found on PATH, it will automatically be
        called afterwards to convert the text files to images.

    pyplantuml-web [pyreverse-options] <package>

        Will use the online form on www.plantuml.com for conversion and
        display the result in your default browser.

        Do NOT use for sensitive data!

Example:

    pyplantumtl -f ALL urllib
        """)
        return False

    target = getTargetPackage(args)

    diadefs = adapter.getDiagramDefinitions(args)
    diadefs = fixDiagramTitle(diadefs, target)

    umls = writer.toPlantUml(diadefs, [])
    for uml in umls:
        umlpath = os.path.abspath(uml)
        print("Created: {0}".format(umlpath))

        # Conversion using the online form.
        if convert_online:
            online.displayOnline(umlpath)
            continue

        images = writer.visualizeLocally(umls)
        for image in images:
            imagepath = os.path.abspath(image)
            print("Created: {0}".format(imagepath))


def convert_local():
    main()


def convert_online():
    main(convert_online=True)
