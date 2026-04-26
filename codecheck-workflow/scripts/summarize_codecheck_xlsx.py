#!/usr/bin/env python3
"""汇总 CodeCheck xlsx 导出单的规则、文件和风险分布。"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


XML_NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

SAFE_RULES = {
    "C0116",
    "G.CMT.06 文件头注释应该包含版权许可信息",
    "G.FMT.01 程序块应该采用4个空格缩进风格编写",
    "G.FMT.02 行宽不超过120个字符",
    "G.FMT.04 用空格突出关键字和重要信息",
    "G.FMT.09 合理的运用换行和缩进",
    "G.CLS.06 类的方法建议统一按照一种规则进行排列",
    "G.CLS.07 类的方法不需要访问实例时，建议定义为staticmethod或classmethod",
    "G.PRJ.05 不用的代码段直接删除，不要注释掉",
    "W0611",
    "W0612",
    "G.CTL.05 建议使用单个下划线代替循环体中未使用的循环变量",
    "C0325",
}


def _iter_shared_strings(zip_file: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zip_file.namelist():
        return []
    root = ET.fromstring(zip_file.read("xl/sharedStrings.xml"))
    return [
        "".join(
            text_node.text or ""
            for text_node in shared_item.iter(
                "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
            )
        )
        for shared_item in root.findall("a:si", XML_NS)
    ]


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = cell.find("a:v", XML_NS)
    if value_node is None:
        inline_node = cell.find("a:is", XML_NS)
        if inline_node is None:
            return ""
        return "".join(
            node.text or ""
            for node in inline_node.iter(
                "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
            )
        )
    raw_value = value_node.text or ""
    if cell_type == "s":
        return shared_strings[int(raw_value)]
    return raw_value


def _load_first_sheet_rows(path: Path) -> tuple[str, list[dict[str, str]]]:
    with zipfile.ZipFile(path) as zip_file:
        workbook = ET.fromstring(zip_file.read("xl/workbook.xml"))
        relationships = ET.fromstring(zip_file.read("xl/_rels/workbook.xml.rels"))
        relationship_map = {
            relationship.attrib["Id"]: relationship.attrib["Target"]
            for relationship in relationships.findall(
                "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
            )
        }
        sheet = workbook.find("a:sheets/a:sheet", XML_NS)
        if sheet is None:
            raise ValueError("xlsx 中没有 worksheet")
        sheet_name = sheet.attrib.get("name", "")
        target = relationship_map[
            sheet.attrib[
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
            ]
        ]
        shared_strings = _iter_shared_strings(zip_file)
        xml_path = f"xl/{target}" if not target.startswith("xl/") else target
        root = ET.fromstring(zip_file.read(xml_path))
        headers: list[str] | None = None
        rows: list[dict[str, str]] = []
        for row in root.findall("a:sheetData/a:row", XML_NS):
            values = [_cell_value(cell, shared_strings) for cell in row.findall("a:c", XML_NS)]
            if headers is None:
                headers = values
                continue
            if not any(values):
                continue
            rows.append(dict(zip(headers, values)))
        return sheet_name, rows


def _normalize_file_path(file_path: str) -> str:
    return str(file_path or "").strip()


def summarize(path: Path, *, top_n: int) -> dict[str, Any]:
    sheet_name, rows = _load_first_sheet_rows(path)
    rule_counter: Counter[str] = Counter()
    tool_counter: Counter[str] = Counter()
    file_counter: Counter[str] = Counter()
    file_rule_counter: defaultdict[str, Counter[str]] = defaultdict(Counter)
    safe_only_files: list[dict[str, Any]] = []
    mixed_files: list[dict[str, Any]] = []

    for row in rows:
        file_path = _normalize_file_path(row.get("文件路径", ""))
        rule_name = str(row.get("规则", "")).strip()
        tool_name = str(row.get("工具名称", "")).strip()
        rule_counter[rule_name] += 1
        tool_counter[tool_name] += 1
        file_counter[file_path] += 1
        file_rule_counter[file_path][rule_name] += 1

    for file_path, counter in file_rule_counter.items():
        distinct_rules = set(counter)
        payload = {
            "file": file_path,
            "count": sum(counter.values()),
            "rules": counter.most_common(top_n),
        }
        if distinct_rules.issubset(SAFE_RULES):
            safe_only_files.append(payload)
            continue
        payload["riskyRules"] = sorted(distinct_rules - SAFE_RULES)
        mixed_files.append(payload)

    safe_only_files.sort(key=lambda item: item["count"], reverse=True)
    mixed_files.sort(key=lambda item: item["count"], reverse=True)

    return {
        "sheetName": sheet_name,
        "totalRows": len(rows),
        "fileCount": len(file_counter),
        "topRules": rule_counter.most_common(top_n),
        "topTools": tool_counter.most_common(top_n),
        "topFiles": [
            {
                "file": file_path,
                "count": count,
                "rules": file_rule_counter[file_path].most_common(top_n),
            }
            for file_path, count in file_counter.most_common(top_n)
        ],
        "safeOnlyFiles": safe_only_files[:top_n],
        "mixedFiles": mixed_files[:top_n],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="汇总 CodeCheck xlsx 导出单。")
    parser.add_argument("xlsx_path", help="CodeCheck 导出单路径")
    parser.add_argument("--top", type=int, default=20, help="每个榜单保留的条目数")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx_path).expanduser().resolve()
    if not xlsx_path.is_file():
        print(json.dumps({"error": f"file not found: {xlsx_path}"}, ensure_ascii=False))
        return 1
    try:
        summary = summarize(xlsx_path, top_n=max(1, int(args.top)))
    except Exception as exc:
        print(
            json.dumps(
                {"error": str(exc), "xlsxPath": str(xlsx_path)},
                ensure_ascii=False,
            )
        )
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
