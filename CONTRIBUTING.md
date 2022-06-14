# Contributing

## Run sanity, unit or integration tests locally

You have to check out the repository into a specific path structure to be able to run `ansible-test`. The path to the git checkout must end with `.../ansible_collections/community/general`. Please see [our testing guide](https://github.com/ansible/community-docs/blob/main/test_pr_locally_guide.rst) for instructions on how to check out the repository into a correct path structure. The short version of these instructions is:

```.bash
mkdir -p ~/dev/ansible_collections/community
git clone https://github.com/ansible-collections/community.general.git ~/dev/ansible_collections/community/general
cd ~/dev/ansible_collections/community/general
```

Then you can run `ansible-test` (which is a part of [ansible-core](https://pypi.org/project/ansible-core/)) inside the checkout. The following example commands expect that you have installed Docker or Podman. Note that Podman has only been supported by more recent ansible-core releases. If you are using Docker, the following will work with Ansible 2.9+.

The following commands show how to run sanity tests:

```.bash
# Run sanity tests for all files in the collection:
ansible-test sanity --docker -v

# Run sanity tests for the given files and directories:
ansible-test sanity --docker -v plugins/modules/system/pids.py tests/integration/targets/pids/
```

The following commands show how to run unit tests:

```.bash
# Run all unit tests:
ansible-test units --docker -v

# Run all unit tests for one Python version (a lot faster):
ansible-test units --docker -v --python 3.8

# Run a specific unit test (for the nmcli module) for one Python version:
ansible-test units --docker -v --python 3.8 tests/unit/plugins/modules/net_tools/test_nmcli.py
```

The following commands show how to run integration tests:

```.bash
# Run integration tests for the interfaces_files module in a Docker container using the
# fedora35 operating system image (the supported images depend on your ansible-core version):
ansible-test integration --docker fedora35 -v interfaces_file

# Run integration tests for the flattened lookup **without any isolation**:
ansible-test integration -v lookup_flattened
```

If you are unsure about the integration test target name for a module or plugin, you can take a look in `tests/integration/targets/`. Tests for plugins have the plugin type prepended.

## pre-commit

To help ensure high-quality contributions this repository includes a [pre-commit](https://pre-commit.com) configuration which
corrects and tests against common issues that would otherwise cause CI to fail. To begin using these pre-commit hooks see
the [Installation](#installation) section below.

This is optional and not required to contribute to this repository.

### Installation

Follow the [instructions](https://pre-commit.com/#install) provided with pre-commit and run `pre-commit install` under the repository base. If for any reason you would like to disable the pre-commit hooks run `pre-commit uninstall`.

This is optional to run it locally.

You can trigger it locally with `pre-commit run --all-files` or even to run only for a given file `pre-commit run --files YOUR_FILE`.

## Useful docs

* [Developing ansible module](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
* [Argument spec](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec)
* [Module documenting](https://docs.ansible.com/ansible/devel/dev_guide/developing_modules_documenting.html)
* [Best practices](https://docs.ansible.com/ansible/devel/dev_guide/developing_modules_best_practices.html)
* [Testing](https://docs.ansible.com/ansible/latest/dev_guide/testing.html)
* [Integration testing](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html)