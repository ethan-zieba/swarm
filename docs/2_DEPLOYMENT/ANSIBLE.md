To have the latest version of ansible, it must be installed using pipx
`pipx install ansible-core`
``

ansible.posix has to be installed using ansible-galaxy: `ansible-galaxy collection install ansible.posix`

Starting the deployment (main_dorian.yml being the base playbook): `ansible-playbook -i inventory.ini main_dorian.yml`

## Needs an overview of the main playbook
