# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
import unittest

from ansible.playbook.task import Task
from ansible.template import Templar

from tests.unit.compat.mock import MagicMock, patch

from plugins.action.echo import ActionModule


class TestEcho_Action(unittest.TestCase):
    def setUp(self):
        task = MagicMock(Task)
        # Ansible > 2.13 looks for check_mode in task
        task.check_mode = False
        task.delegate_to = False
        play_context = MagicMock()
        # Ansible <= 2.13 looks for check_mode in play_context
        play_context.check_mode = False
        connection = MagicMock()
        fake_loader = {}
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(
            task=task,
            connection=connection,
            play_context=play_context,
            loader=fake_loader,
            templar=templar,
            shared_loader_obj=None,
        )
        self._plugin.get_distribution = MagicMock()
        self._plugin.get_distribution.return_value = {
            'name': 'ubuntu',
            'version': '20',
            'family': 'debian'
        }
        self._plugin._low_level_execute_command = MagicMock()
        self._plugin._low_level_execute_command.return_value = {
            'rc': 0,
            'stdout': '',
            'stdout_lines': [],
            'stderr': '',
            'stderr_lines': [],
        }
        self._plugin._task.action = "echo"
        self._task_vars = {"inventory_hostname": "mockdevice"}

    def test_argspec_no_updates(self):
        """Check passing invalid argspec"""
        self._plugin._task.args = {}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result == {
            'echo': True,
            'changed': True,
            'echo_command': 'echo Echo initiated by Ansible'
        }

    def test_success(self):
        """Check passing invalid argspec"""
        self._plugin._task.args = {"msg": "Custom message"}
        result = self._plugin.run(task_vars=self._task_vars)
        assert result == {
            'echo': True,
            'changed': True,
            'echo_command': 'echo Custom message'
        }
