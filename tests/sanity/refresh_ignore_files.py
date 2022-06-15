#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type
from itertools import chain
from pathlib import Path

target_dir = Path('.')

ignore_dir = target_dir / "tests" / "sanity"
module_dir = target_dir / "plugins" / "modules"
module_utils_dir = target_dir / "plugins" / "module_utils"
ignore_dir.mkdir(parents=True, exist_ok=True)

PYTHON_IGNORES = ["2.6", "2.7", "3.5", "3.6"]

for minor_version in [9, 10, 11, 12, 13, 14]:
    ignore_any = ignore_dir / "ignore-any.txt"
    ignore_file = ignore_dir / f"ignore-2.{minor_version}.txt"
    if ignore_file.exists():
        ignore_content = ignore_file.read_text().split("\n")
    else:
        ignore_content = []
    ignore_content.extend(ignore_any.read_text().split("\n"))
    ignore_content.append("tests/sanity/refresh_ignore_files.py shebang!skip")

    skip_list = [
    ]
    if minor_version < 12:
        skip_list.extend([
            "future-import-boilerplate!skip",  # Py2 only
            "metaclass-boilerplate!skip",  # Py2 only
        ])
        skip_list.extend([f'compile-{py}!skip' for py in PYTHON_IGNORES])
        skip_list.extend([f'import-{py}!skip' for py in PYTHON_IGNORES])

    files = chain(
        module_dir.glob("*.py"),
        module_utils_dir.glob("*.py")
    )

    for f in files:
        if f.is_symlink():
            continue
        for test in skip_list:
            ignore_content.append(f"{f} {test}")

    ignore_file.write_text("\n".join(sorted(set(ignore_content))).lstrip("\n"))
