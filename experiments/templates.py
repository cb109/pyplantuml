EMPTY = "\n"

STARTUML = "@startuml\n"

ENDUML = "@enduml\n"

TITLE = "title {name}\n"

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

CLASS = """
class {0} {
    {1}
}
"""

METHOD = "{returnValue} {name}()\n"