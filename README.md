# Ansible Collection - linkybook.utils

This is a skeleton collection containing a cliconf plugin and a terminal plugin
suitable for modifying for use on new unsupported platforms to get cli_command
working.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

For example, the playbook

```
---
- hosts: linux
  connection: network_cli
  gather_facts: false

  vars:
    ansible_network_os: linkybook.utils.linux

  tasks:
    - name: Run a command
      cli_command:
        command: "uname -a"
```

will produce something like the following output

```
% ansible-playbook -v linux.yaml

PLAY [linux] *******************************************************************************

TASK [Run a command] ***********************************************************************
ok: [remote] => changed=false
  stdout: |-
    Linux remote 4.19.0-20-amd64 #1 SMP Debian 4.19.235-1 (2022-03-17) x86_64 GNU/Linux
    %
  stdout_lines: <omitted>

PLAY RECAP *********************************************************************************
remote                     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

This is customized to be used against my personal servers, so you should look
through the cliconf and terminal plugins to adapt them to your own uses

## Included content

<!--start collection content-->
### Cliconf plugins
Name | Description
--- | ---
[linkybook.utils.linux](https://github.com/Qalthos/linkybook.utils/blob/main/docs/linkybook.utils.linux_cliconf.rst)|Example bare minimum cliconf plugin

<!--end collection content-->


## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
