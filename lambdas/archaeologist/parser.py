from dataclasses import dataclass, field
from typing import Dict, List

import tree_sitter_python
from tree_sitter import Language, Node, Parser

_LANGUAGE = Language(tree_sitter_python.language())
_PARSER = Parser(_LANGUAGE)


@dataclass
class ParseResult:
    chunks: List[dict] = field(default_factory=list)
    symbol_map: Dict[str, List[str]] = field(default_factory=dict)


def _text(node: Node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _extract_docstring(definition: Node, source: bytes) -> str | None:
    body = definition.child_by_field_name("body")
    if body is None:
        return None
    for child in body.named_children:
        if child.type == "expression_statement":
            inner = child.named_children[0] if child.named_children else None
            if inner is not None and inner.type == "string":
                raw = _text(inner, source)
                return raw.strip().strip("'\"")
        return None
    return None


def _dotted_name(node: Node, source: bytes) -> str:
    return _text(node, source)


def _record_import(symbol_map: Dict[str, List[str]], module: str, name: str) -> None:
    symbol_map.setdefault(module, []).append(name)


def _handle_import_statement(node: Node, source: bytes, symbol_map: Dict[str, List[str]]) -> None:
    for child in node.named_children:
        if child.type == "dotted_name":
            module = _dotted_name(child, source)
            _record_import(symbol_map, module, module)
        elif child.type == "aliased_import":
            name_node = child.child_by_field_name("name")
            alias_node = child.child_by_field_name("alias")
            if name_node is None:
                continue
            module = _dotted_name(name_node, source)
            alias = _text(alias_node, source) if alias_node is not None else module
            _record_import(symbol_map, module, alias)


def _handle_import_from_statement(node: Node, source: bytes, symbol_map: Dict[str, List[str]]) -> None:
    module_node = node.child_by_field_name("module_name")
    module = _dotted_name(module_node, source) if module_node is not None else ""

    for child in node.named_children:
        if child == module_node:
            continue
        if child.type == "dotted_name":
            _record_import(symbol_map, module, _dotted_name(child, source))
        elif child.type == "aliased_import":
            name_node = child.child_by_field_name("name")
            alias_node = child.child_by_field_name("alias")
            if name_node is None:
                continue
            imported = _text(alias_node, source) if alias_node is not None else _dotted_name(name_node, source)
            _record_import(symbol_map, module, imported)
        elif child.type == "wildcard_import":
            _record_import(symbol_map, module, "*")


def _parse_file(file_path: str, result: ParseResult) -> None:
    with open(file_path, "rb") as f:
        source = f.read()

    tree = _PARSER.parse(source)
    root = tree.root_node

    for node in root.named_children:
        if node.type in ("function_definition", "class_definition"):
            name_node = node.child_by_field_name("name")
            if name_node is None:
                continue
            result.chunks.append({
                "name": _text(name_node, source),
                "kind": "function" if node.type == "function_definition" else "class",
                "docstring": _extract_docstring(node, source),
                "source": _text(node, source),
                "file_path": file_path,
            })
        elif node.type == "import_statement":
            _handle_import_statement(node, source, result.symbol_map)
        elif node.type == "import_from_statement":
            _handle_import_from_statement(node, source, result.symbol_map)


def parse_manifest(manifest: dict) -> ParseResult:
    result = ParseResult()
    for file_path in manifest["files"]:
        try:
            _parse_file(file_path, result)
        except (OSError, UnicodeDecodeError):
            continue
    return result
