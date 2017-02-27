# Cisco Tech Day SF

**Nexus Automation and Orchestration using DevOPS Tools**

All scripts for Techday demo


## Ansible Demo

### Host file
[Host file](hosts)

### Example 1 - Simple Ansible playbook to Create single vlan on Cisco NXOS switch

[vlan example 1](vlan-example-1.yml)

### Example 2  - Simple Ansible playbook to Create Multiple vlan on Cisco NXOS switch

[vlan example 2](vlan-example-2.yml)

### Example 3  - Ansible playbook to Create Multiple vlan on Cisco NXOS switch using data file

[vlan example 3](vlan-example-3.yml)

[vlan list file ](vlan_list.yml)

### Example 4 - Orchestration Example

[vlan example 4](vlan-example-4.yml)

[switch port list ](port_list.yml)


### Example 5 - Orchestration Example with Host specific Variables

[vlan example 4](vlan-example-5.yml)

Host specific variables are kept in a special folder called `host_vars`.  Just create a yml file with the same name as your host and add all the variables specific to this host in this file.

[Host specific Variable ](/host_vars/n9k-1.yml)


### Jenkins Login

. update the host file too to include your network devices ..n9k-1

` docker exec -it jenkins-ansible /bin/bash `

vim /etc/hosts  and add  172.16.123.100  n9k-1
