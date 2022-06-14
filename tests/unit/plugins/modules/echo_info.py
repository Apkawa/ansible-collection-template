from plugins.modules import echo_info
from tests.unit.utils import ModuleTestCase, AnsibleFailJson, set_module_args, AnsibleExitJson


class TestEcho_Info(ModuleTestCase):
    """Main class for testing dnsimple module."""

    def setUp(self):
        """Setup."""
        super(TestEcho_Info, self).setUp()
        self.module = echo_info

    def tearDown(self):
        """Teardown."""
        super(TestEcho_Info, self).tearDown()

    def test_with_no_parameters(self):
        """Failure must occurs when all parameters are missing"""
        with self.assertRaises(AnsibleFailJson) as exc_info:
            set_module_args({})
            self.module.main()
        assert exc_info.exception.args[0] == {
            'msg': 'missing required arguments: messages', 'failed': True
        }

    def test_echo(self):
        """key and account will pass, returns domains"""
        with self.assertRaises(AnsibleExitJson) as exc_info:
            set_module_args({
                'messages': ['foo']
            })
            self.module.main()
        result = exc_info.exception.args[0]
        assert result == {
            'messages': ['foo'], 'changed': False
        }

    def test_empty_message(self):
        """key and account will pass, returns domains"""
        with self.assertRaises(AnsibleFailJson) as exc_info:
            set_module_args({
                'messages': []
            })
            self.module.main()
        result = exc_info.exception.args[0]
        assert result == {
            'msg': 'messages is empty!', 'messages': [], 'failed': True
        }
