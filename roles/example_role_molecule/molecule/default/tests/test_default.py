# -*- coding: utf-8 -*-
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_cron_generated(host):
    f = host.file("/tmp/test")
    assert f.exists
    assert f.content == 'EXAMPLE=molecule'
