# Repo used for the demo site 6.demo.plone.org

This is the repository used in Plone 6 demo in 6.demo.plone.org.

You can find the backend in the `/api` folder, and the frontend in the root of the repo.
You can find also convenience scripts in the supplied `Makefile`.

For convenience the deployment Ansible playbooks are included in the `ansible` folder.
 They install the entire required dependencies and infrastructure as well as the services.

For any questions, please contact the @plone/ai-team

## Ansible Usage

Checkout and work with this repository.

```shell
git clone https://github.com/plone/6.demo.plone.org.git
cd 6.demo.plone.org.git
# git checkout ansible # for testing this branch only
```

Create a Python virtual environment, upgrade its package management tools, and install Ansible into it.

```shell
python3 -m venv env
env/bin/pip install --upgrade pip setuptools
env/bin/pip install ansible
```

Create or reuse an existing SSH key to deploy into a virtual machine in the next step.

```shell
ssh-keygen
```

Create a remote virtual machine for production deployment, such as a Digital Ocean droplet or AWS EC2 instance.


[//]: # (I created a DO droplet of 1GB RAM, and I expect it to fail.)
[//]: # (The droplet might need to be resized.)

This playbook has been tested on Ubuntu 20.04 LTS only.
The minimum requirements for the virtual machine include ___GB memory.
Obtain the hostname of your virtual machine.
This process is left to the provider to document.

Update the Ansible configuration file at `ansible/vbox_host.cfg` with your hostname, replacing the value of `<name_of_your_host>`.

Run the playbook.

```shell
env/bin/ansible-playbook -i ansible/vbox_host.cfg ansible/volto-demo.yml

PLAY [all] *************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
fatal: [143.198.238.54]: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host 127.0.0.1 port 2222: Connection refused", "unreachable": true}

PLAY RECAP *************************************************************************************************************
143.198.238.54             : ok=0    changed=0    unreachable=1    failed=0    skipped=0    rescued=0    ignored=0
```

*sad trombone*