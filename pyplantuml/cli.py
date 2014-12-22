import os
import sys
import pprint

from pyplantuml import adapter
from pyplantuml import writer


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


def main():
    args = sys.argv[1:]
    if not args:
        print ("""
pyplantuml
----------

usage:

    pyplantuml [pyreverse-options] [--] [plantuml-options] <package>

example:

    pyplantumtl -f ALL -- -w 1024 -h 512 urllib
        """)
        return 1

    # TODO: Make this have an effect
    # if "--" in args:
    #     idx = args.index("--")
    #     pyreverseArgs = args[:idx]
    #     plantumlArgs = args[idx:]
    # else:
    #     pyreverseArgs, plantumlArgs = args, []

    target = getTargetPackage(args)

    diadefs = adapter.getDiagramDefinitions(args)
    diadefs = fixDiagramTitle(diadefs, target)

    umls = writer.toPlantUml(diadefs, [])  # TODO use plantumlArgs instead of []
    images = writer.visualize(umls)

    pprint.pprint(images)


if __name__ == "__main__":
    main()