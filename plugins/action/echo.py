# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleConnectionFailure, AnsibleActionFail
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

from ..module_utils.common.argspec_validate import check_argspec
from ..modules.echo import DOCUMENTATION

display = Display()


class TimedOutException(Exception):
    pass


class ActionModule(ActionBase):
    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset(("msg",))

    DEFAULT_CONNECT_TIMEOUT = None
    DEFAULT_PRE_SHUTDOWN_DELAY = 0
    DEFAULT_SHUTDOWN_MESSAGE = "Shut down initiated by Ansible"
    DEFAULT_ECHO_COMMAND = "shutdown"
    DEFAULT_SHUTDOWN_COMMAND_ARGS = ""
    DEFAULT_SUDOABLE = False

    SHUTDOWN_COMMANDS = {
        "alpine": "poweroff",
        "vmkernel": "halt",
    }

    COMMAND_ARGS = {
        "alpine": "",
        "void": "void ",
        "freebsd": "freebsd ",
        "linux": DEFAULT_ECHO_COMMAND,
        "macosx": "",
        "openbsd": '-h +{delay_min} "{message}"',
        "solaris": '-y -g {delay_sec} -i 5 "{message}"',
        "sunos": '-y -g {delay_sec} -i 5 "{message}"',
        "vmkernel": "-d {delay_sec}",
        "aix": "-Fh",
    }

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)

    def _get_value_from_facts(self, variable_name, distribution, default_value):
        """
        Get dist+version specific args first, then distribution, then family, lastly use default
        """
        # TODO Move to helpers
        attr = getattr(self, variable_name)
        value = attr.get(
            distribution["name"] + distribution["version"],
            attr.get(
                distribution["name"], attr.get(distribution["family"], getattr(self, default_value))
            ),
        )
        return value

    def get_distribution(self, task_vars):
        # TODO Move to helpers
        # FIXME: only execute the module if we don't already have the facts we need
        distribution = {}
        display.debug(
            "{action}: running setup module to get distribution".format(action=self._task.action)
        )
        module_output = self._execute_module(
            task_vars=task_vars,
            module_name="ansible.legacy.setup",
            module_args={"gather_subset": "min"},
        )
        try:
            if module_output.get("failed", False):
                raise AnsibleError(
                    "Failed to determine system distribution. {0}, {1}".format(
                        to_native(module_output["module_stdout"]).strip(),
                        to_native(module_output["module_stderr"]).strip(),
                    )
                )
            distribution["name"] = module_output["ansible_facts"]["ansible_distribution"].lower()
            distribution["version"] = to_text(
                module_output["ansible_facts"]["ansible_distribution_version"].split(".")[0]
            )
            distribution["family"] = to_text(
                module_output["ansible_facts"]["ansible_os_family"].lower()
            )
            display.debug(
                "{action}: distribution: {dist}".format(action=self._task.action, dist=distribution)
            )
            return distribution
        except KeyError as ke:
            raise AnsibleError(
                'Failed to get distribution information. Missing "{0}" in output.'.format(
                    ke.args[0]
                )
            )

    def _check_argspec(self):
        valid, argspec_result, self._task.args = check_argspec(
            DOCUMENTATION, name=self._task.action, schema_conditionals=None, **self._task.args
        )
        return valid, argspec_result

    def perform_cmd(self, task_vars, distribution):
        result = {}
        cmd_result = {}

        echo_args = self._task.args["msg"]
        echo_exc = "echo " + echo_args

        self.cleanup(force=True)
        try:
            display.vvv("{action}: echo...".format(action=self._task.action))
            display.debug(
                "{action}: echo '{command}'".format(action=self._task.action, command=echo_args)
            )
            if self._play_context.check_mode:
                cmd_result["rc"] = 0
            else:
                cmd_result = self._low_level_execute_command(
                    echo_exc, sudoable=self.DEFAULT_SUDOABLE
                )
        except AnsibleConnectionFailure as e:
            # If the connection is closed too quickly due to the system being shutdown, carry on
            display.debug(
                "{action}: AnsibleConnectionFailure caught and handled: {error}".format(
                    action=self._task.action, error=to_text(e)
                )
            )
            cmd_result["rc"] = 0

        if cmd_result["rc"] != 0:
            result["failed"] = True
            result["shutdown"] = False
            result["msg"] = "Echo failed. Error was {stdout}, {stderr}".format(
                stdout=to_native(cmd_result["stdout"].strip()),
                stderr=to_native(cmd_result["stderr"].strip()),
            )
            return result

        result["failed"] = False
        result["echo_command"] = echo_exc
        return result

    def run(self, tmp=None, task_vars=None):
        self._supports_check_mode = True
        self._supports_async = True
        # If running with local connection, fail so we don't shutdown ourself
        if self._connection.transport == "local" and (not self._play_context.check_mode):
            msg = "Running {0} with local connection would shutdown the control node.".format(
                self._task.action
            )
            return {"changed": False, "elapsed": 0, "shutdown": False, "failed": True, "msg": msg}

        if task_vars is None:
            task_vars = {}

        valid, errors = self._check_argspec()
        if not valid:
            return errors

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get("skipped", False) or result.get("failed", False):
            return result

        distribution = self.get_distribution(task_vars)

        cmd_result = self.perform_cmd(task_vars, distribution)

        if cmd_result["failed"]:
            result = cmd_result
            return result

        result["echo"] = True
        result["changed"] = True
        result["echo_command"] = cmd_result["echo_command"]
        return result
