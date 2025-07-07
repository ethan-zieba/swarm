## Summary

Our Ansible provisions a GlusterFS shared volume, a Docker Swarm cluster with a Docker volume backed by GFS

## Installing Ansible

To have the latest version of ansible, it must be installed using pipx
`pipx install ansible-core`

ansible.posix has to be installed using ansible-galaxy: `ansible-galaxy collection install ansible.posix`
And: `ansible-galaxy collection install community.docker`

## Deployment

Starting the deployment (main_dorian.yml being the base playbook): `ansible-playbook -i inventory.ini main_dorian.yml`

**Docker Repository installation fix**: We had a problem where the Docker gpg key was not dearmored and so the repository couldn't be signed and accepted by apt.
This resulted in the deployment of anything requiring apt crashing because it couldn't update the cache.
We found out that apt-key was deprecated, and that we must now use: `ansible.builtin.deb822_repository`

## Ansible files overview
```
├── inventory.ini
├── main_dorian.yml
└── roles
    ├── docker_swarm
    │   ├── defaults
    │   │   └── main.yml
    │   └── tasks
    │       ├── init_manager.yml
    │       ├── join_worker.yml
    │       ├── main.yml
    │       └── volume.yml
    └── glusterfs
        ├── defaults
        │   └── main.yml
        └── tasks
            ├── configure.yml
            ├── install.yml
            ├── main.yml
            └── mount.yml
```
## Misc knowledge

### Roles

A role is a structured way to organize playbooks by function. It lets you reuse configuration logic in a modular, readable, and maintainable format.
Each role usually represents one responsibility: i.e: installing Docker, configuring a GlusterFS brick, or joining a Swarm.
Each role is a folder with a default internal structure:
- tasks
- handlers
- templates
- files
- vars
- defaults
- meta

Not every internal folder of a role has to be used, only `tasks` is enough for basic roles.

#### Benefits of using roles

Cleaner ansible structure
Reusable tasks and functions
More readable
Integration with Ansible Galaxy

#### To use a role in a playbook

```
- name: Set up Docker
  hosts: all
  become: true
  roles:
    - docker
```
