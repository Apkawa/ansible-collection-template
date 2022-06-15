#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
module: echo_info
short_description: Example module
description:
  - For example
author:
    - Apkawa (@apkawa)
options:
  messages:
    type: list
    elements: str
    required: true
    description: >
        list of messages

"""

EXAMPLES = """
- name: Example echo
  apkawa_collection_template.echo_info:
    messages:
        - foo
        - bar
"""

RETURN = """
messages:
  description: path to python version used
  returned: always
  type: list
  sample:
    - foo
    - bar
"""

from ansible.module_utils.basic import AnsibleModule

# https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec
ARGUMENT_SPEC = dict(messages=dict(type="list", elements="str", required=True))


def main():
    module = AnsibleModule(
        argument_spec=ARGUMENT_SPEC,
        supports_check_mode=True,
    )
    if not module.params["messages"]:
        module.fail_json(msg="messages is empty!", messages=module.params["messages"])
        return

    module.exit_json(messages=module.params["messages"])


if __name__ == "__main__":
    main()
