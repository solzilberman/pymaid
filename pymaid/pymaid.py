import ast
import os
import sys
import glob
import argparse

from utils import BASE_MJS_STRING, TAB
from mermaid import MermaidCode


def read_py_file(filename: str):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf8") as f:
            return f.read()


def get_ast(filename: str):
    return ast.parse(read_py_file(filename))


def visitNode(node, tree: list):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            tree.append(
                {
                    child.name: {
                        "attributes": [],
                        "methods": [],
                    }
                }
            )
            visitNode(child, tree)
        if isinstance(child, ast.FunctionDef):
            tree[-1][node.name]["methods"].append(child.name)
        if isinstance(child, ast.Assign):
            tree[-1][node.name]["attributes"].append(child.targets[0].id)
    return tree


def get_all_classes_from_single_file(tree) -> list:
    return [
        ast_object
        for ast_object in ast.walk(tree)
        if isinstance(ast_object, ast.ClassDef)
    ]


def get_all_classes(path) -> list:
    all_classes = []
    for filename in glob.glob(path):
        tree = get_ast(filename)
        all_classes += [*get_all_classes_from_single_file(tree)]
    return all_classes


def tab_over(section: str) -> str:
    # ret[:-1] to remove extra newline
    return "".join([f"{TAB}{line}\n" for line in section.splitlines()])[:-1]


def pack_final_code(body: str) -> str:
    return f"{BASE_MJS_STRING}{tab_over(body)}\n\n"


def safe_id_parse(obj):
    try:
        return obj.id
    except AttributeError:
        return None


def check_id_exists(obj):
    return getattr(obj, "id", None) is not None


def parse_parents(d, c):
    # https://stackoverflow.com/questions/72064609
    def parse_chain(d, c, p=[]):
        if isinstance(d, ast.Name):
            return [d.id] + p
        if isinstance(d, ast.Call):
            for i in d.args:
                parse_parents(i, c)
            return parse_chain(d.func, c, p)
        if isinstance(d, ast.Attribute):
            return parse_chain(d.value, c, [d.attr] + p)

    if isinstance(d, (ast.Call, ast.Attribute)):
        a = parse_chain(d, c)
        c.append(".".join(a if a else []))
    else:
        for i in getattr(d, "_fields", []):
            if isinstance(t := getattr(d, i), list):
                for i in t:
                    parse_parents(i, c)
            else:
                parse_parents(t, c)


def get_all_bases(cls):
    nested_inheritance = []
    for base in cls.bases:
        if isinstance(base, ast.Attribute):
            res = []
            parse_parents(base, res)
            nested_inheritance += list(map(lambda x: x.split(".")[-1], res))
    targets = nested_inheritance + [
        base.id for base in cls.bases if check_id_exists(base)
    ]
    return {
        "source": get_class_name(cls),
        "targets": targets,
    }


def get_init_method(cls):
    for node in ast.walk(cls):
        if isinstance(node, ast.ClassDef):
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef) and subnode.name == "__init__":
                    return subnode


def get_method_args(method):
    arg_dict = {}
    for arg in method.args.args:
        if arg.annotation is not None:
            arg_dict[arg.arg] = arg.annotation
    return arg_dict


def get_assignments(method):
    assignments = {}
    for node in ast.walk(method):
        if isinstance(node, ast.Assign):
            if (
                isinstance(node.targets[0], ast.Attribute)
                and safe_id_parse(node.targets[0].value) == "self"
            ):
                assignments[node.targets[0].attr] = (
                    node.value.id if getattr(node.value, "id", None) is not None else ""
                )
    return assignments


def get_all_method_names(cls):
    method_names = []
    for node in ast.walk(cls):
        if isinstance(node, ast.ClassDef):
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    method_names.append(subnode.name)
    return method_names


def generate_type_map(class_dict, init_args) -> dict:
    base = class_dict["name"]
    targets = set()
    for attr in class_dict["attributes"].values():
        if attr in init_args and check_id_exists(init_args[attr]):
            targets.add(init_args[attr].id)
    return {"source": base, "targets": list(targets)}


def get_class_name(cls):
    return cls.name


def parse_args(args):
    arg_parser = argparse.ArgumentParser(description="PyMaid version 0.0.1")
    # arg_parser.usage = "pymaid -i <input> -o <output>"
    arg_parser.add_argument(
        "-i", "--input", help="Input file or glob", required=True, metavar=''
    )
    arg_parser.add_argument(
        "-o", "--output", help="Output file to write to", default="out.md",metavar=''
    )
    arg_parser.usage = arg_parser.format_help()
    return arg_parser.parse_args()

def run():
    opts = parse_args(sys.argv[1:])
    mjscode = MermaidCode()
    classes = get_all_classes(opts.input)
    for _class in classes:
        class_name = get_class_name(_class)
        bases = get_all_bases(_class)
        init = get_init_method(_class)
        init_args = get_method_args(init)
        self_attributes = get_assignments(init)
        methods = get_all_method_names(_class)
        class_dict = {
            "name": class_name,
            "attributes": self_attributes,
            "methods": methods,
            "bases": bases,
        }
        t_map = generate_type_map(class_dict, init_args)
        mjscode.add_relationship(bases, "inheritance")
        mjscode.add_relationship(t_map, "aggregation")
        mjscode.add_class(class_dict)

    mjscode.save(opts.output)
    
