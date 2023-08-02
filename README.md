# Ansible Nokia ISAM FTTN 7330 Collection
This collection is a fork of https://github.com/Qalthos/linkybook.utils which describes the skeleton of a network device collection. It also uses https://github.com/ansible-network/cli_rm_builder to scaffold the ressource module folders and boiler code.

This Ansible Collection contains modules to manage Nokia ISAM FTTN 7330 devices. The Nokia ISAM FTTN Line-up is of the Device Type MSAN. Most of the options available are for different types of OSI Layer 2 protocols. As such it is very different from other Ansible Network Collections whcih are specialised on routers and switches. This repository is under active development and not yet ready for production use! It is not supported by  nor affiliated to Nokia in any way! Use at your own risk!


Currently available modules are:
* cli_command
* cli_config
* isam_interfaces

Future modules will include:
* isam_bridges
* isam_ethernet_ont
* isam_facts
* isam_ont_interfaces
* isam_ont_slots
* isam_ping
* isam_qos_interfaces
* isam_vlans

## Requirements & Installation
### Requirements
* Ansible 2.9 or higher
* Python 3.6 or higher
* Nokia ISAM FTTN 7330 device running ISAM Release R6.2.04m
 or higher

### Installation
Install the collection from Github:
```
git clone https://github.com/jahknem/nokia.isam.git
cd nokia.isam
pip3 install -r requirements.txt
ansible-galaxy collection build
ansible-galaxy collection install isam-isam-*.tar.gz
```
### Usage

To use this collection the following needs to be added to the inventory:
```
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: isam.isam.isam
```
Some modules take a long time to complete due to the slow nature of the device. To increase the timeout for these modules the following can be added to the inventory:
```
ansible_command_timeout : 150
```
150 Seconds should be enough to complete a transmission of the complete configuration. As such it should also be enough for most other commands. (Note: cli_config pulls the entire flat config, so it can take 10+ minutes to execute for a highly populated OLT) Consider using cli_command instead if diff isn't needed.

   #### Sample Playbook
   ```
   ---
   - name: Nokia Github isam Plugin example test
     hosts: localhost
     connection: network_cli
     gather_facts: false
   
     vars:
       ansible_user: "yourUserNameHere"
       ansible_ssh_pass: "yourPassword"
       ansible_persistent_log_messages: false
       ansible_connection: ansible.netcommon.network_cli
       ansible_network_os: isam.isam.isam
       ansible_command_timeout : 150
       test_olt: "MyLab-TestOLT-1"
   
     tasks:
       - name: Example command to show the software version on the OLT
         cli_command:
           command: "show software-mngt version ansi"
         delegate_to: "{{test_olt}}"
         register: command_1
   
       - name: Print return information
         ansible.builtin.debug:
           msg:
           - "command {{command_1}}"
 
       - name: Multi-line command
         ansible.netcommon.cli_command:
           command: |
             configure bridge port 1/1/1/1/1/1/1 pvid 1
             configure bridge port 1/1/1/1/1/1/2 pvid 1
         delegate_to: "{{test_olt}}"
         tags: always

      - name: multiline config
        ansible.netcommon.cli_config:
          config: |
            configure bridge port 1/1/1/1/1/1/2 vlan-id 1
            configure bridge port 1/1/1/1/1/1/2 pvid 1
          diff_match: none
          diff_replace: block #block does all lines
        delegate_to: "{{test_olt}}"

      - name: Push file
        ansible.netcommon.cli_command:
          command: "{{ lookup('file', './test-command.txt') }}"
        delegate_to: "{{test_olt}}"
        tags: always
   ```
