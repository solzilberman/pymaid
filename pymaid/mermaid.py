from utils import (
    BASE_MJS_STRING,
    LBRACKET,
    RBRACKET,
    TAB,
    CODE_WRAP_START,
    CODE_WRAP_END,
)


class MermaidCode:
    def __init__(self):
        self.mjs_str = BASE_MJS_STRING
        self.class_str = ""
        self.relationship_str = ""

    def add_class(self, cls: dict):
        self.class_str += class_to_mermaid(cls)

    def add_relationship(self, rel: dict, _type: str):
        if _type == "aggregation":
            self.relationship_str += aggregation_relationship_to_mermaid(rel)
        elif _type == "inheritance":
            self.relationship_str += inheritance_relationship_to_mermaid(rel)

    def save(self, filename: str):
        final_string = f"{self.mjs_str}{self.relationship_str}{self.class_str}"
        final_string = f"{CODE_WRAP_START}{final_string}{CODE_WRAP_END}"
        with open(filename, "w") as f:
            print(final_string, file=f)


def class_to_mermaid(cls: dict) -> str:
    name = cls["name"]
    mjs_str = f"{TAB}class {name}{LBRACKET}\n"
    for attr in cls["attributes"]:
        bullet = generate_bullet_from_name(attr)
        mjs_str += f"{TAB*2}{bullet}{attr}\n"
    for func in cls["methods"]:
        bullet = generate_bullet_from_name(func)
        mjs_str += f"{TAB*2}{bullet}{func}()\n"
    mjs_str += f"{TAB*2}{RBRACKET}\n"
    return mjs_str


def aggregation_relationship_to_mermaid(rel: dict) -> str:
    all_connections = ""
    for target in rel["targets"]:
        all_connections += f"{TAB}{rel['source']} --o {target}\n"
    return all_connections


def inheritance_relationship_to_mermaid(rel: dict) -> str:
    all_connections = ""
    for target in rel["targets"]:
        all_connections += f"{TAB}{target} <|-- {rel['source']}\n"
    return all_connections


def generate_bullet_from_name(name: str) -> str:
    if name[:2] == "__":
        return "~"
    elif name[:1] == "_":
        return "-"
    else:
        return "+"
