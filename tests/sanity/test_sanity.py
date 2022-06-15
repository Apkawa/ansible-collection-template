# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import subprocess
import sys

import pytest
from _pytest.config import Config


def run(environment, pytestconfig: Config):
    __tracebackhide__ = True
    os.chdir(pytestconfig.rootpath)
    args = [
        "ansible-test",
        "sanity",
        "--requirements",
        "--color",

    ]
    python_version = ".".join(map(str, sys.version_info[:2]))
    args.extend(["--python", python_version])

    process = subprocess.run(
        args=args,
        env=environment,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        check=False,
        shell=False,
    )
    if process.returncode:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))

        pytest.fail(reason="Sanity test failed")


def test_sanity(environment, pytestconfig):
    run(environment=environment, pytestconfig=pytestconfig)
