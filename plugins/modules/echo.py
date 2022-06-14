#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
module: echo
short_description: Example action
notes:
  - C(PATH) is ignored on the remote node when searching for the C(shutdown) command. Use I(search_paths)
    to specify locations to search if the default paths do not work.
description:
    - Example
version_added: "1.1.0"
options:
  msg:
    description:
      - Message to display to users before shutdown.
    type: str
    required: yes

seealso:
- module: ansible.builtin.reboot
author:
    - Apkawa <apkawa@gmail.com>
'''

EXAMPLES = r'''
- name: Example echo
  apkawa.collection_template.echo:

- name: Delay shutting down the remote node
  apkawa.collection_template.echo:
    msg: "Foo"

'''

RETURN = r'''
echo:
  description: C(true) if the machine has been shut down.
  returned: always
  type: bool
  sample: true
'''
