# Docker Swarm
## Project for La Plateforme_
*but mostly for me*

### Statement

Deploy a full Docker Swarm cluster with an NFS storage.

* * *

# TTICHAN GraSP CloG
(Yes, that is how we will refer to this project from now on)
## Project Summary

- Traeffik - Reverse Proxy for accessing the services
- T.O.M - Tracking & Observation Microagent
- InfluxDB - For indexing the N.A.D.I.R logs
- Clavister - Physical firewall
- H.U.G.O - Highly-compressed Upload for Guaranteed Offsite storage
- Ansible - For provisionning the Pi 4's
- N.A.D.I.R - Network Anomaly Detection and Intrusion Reporter

- Grafana - For the InfluxDB logs visualisation
- Swarm - Multi-nodes cluster for orchestrating docker containers
- Portainer - Graphical interface for managing the Swarm

- Cloudflare - For creating a tunnel
- GlusterFS - Replicated and distributed storage

# Traeffik

# T.O.M

Microagent in python, monitors the .bash_history of the 3 Docker Swarm nodes 
Can monitor any log file, as well as SSH connections

# InfluxDB

SQL-like database easy to use and powerful for storing and indexing logs
Easier than Prometheus and more lightweight and straightforward

# Clavister

Swedish firewall company
We use an E10 firewall

# H.U.G.O

Bash script compressing the GlusterFS brick and sending it to a cloud storage

# Ansible

Running the full setup (working directory is the one with the inventory and playbooks): `ansible-playbook -i inventory.ini dorian.yml`
This will provision a 3-node GlusterFS cluster, a Docker Swarm, and a shared Docker volume backed by GlusterFS
Docker Repository installation fix: We had a problem where the Docker gpg key was not dearmored and so the repository couldn't be signed and accepted by apt.
This resulted in the deployment of anything requiring apt crashing because it couldn't update the cache.
We found out that apt-key was deprecated, and that we must now use: ansible.builtin.deb822_repository

## Our Ansible configuration

```
directory/
├── inventory.ini
├── site.yml # master playbook
└── roles
    ├── docker
    │   └── tasks
    │       └── main.yml # installs docker and enables the service
    ├── glusterfs
    │   └── tasks
    │       ├── configure.yml # probes for SwagPi1 and SwagPi2 until they are connected, then creates volume gv0 from the bricks, starts the volume
    │       ├── install.yml # installs and enables glusterfs and creates a brick directory
    │       ├── main.yml # starts install.yml
    │       └── mount.yml # installs FUSE client, creates mount point and mounts the GlusterFS volume to it
    └── swarm
        └── tasks
            ├── init_manager.yml # initiates swarm manager, gets worker token
            ├── join_worker.yml # runs on each worker host, joins the cluster
            ├── main.yml
            └── volume.yml # creates GlusterFS subdir for Docker, and Docker Swarm volume backed by GFS
```

## Ansible key concepts

### Roles

A role is a structured way to organize playbooks by function. It lets you reuse configuration logic in a modular, readable, and maintainable format.
Each role usually represents one responsibility: i.e: installing Docker, configuring a GlusterFS brick, or joining a Swarm.
Each role is a folder with a default internal structure:
tasks
handlers
templates
files
vars
defaults
meta

Not every internal folder of a role has to be used, only `tasks` is enough for basic roles.

To use a role in a playbook:
```
- name: Set up Docker
  hosts: all
  become: true
  roles:
    - docker
```

#### Benefits of using roles

Cleaner ansible structure
Reusable tasks and functions
More readable
Integration with Ansible Galaxy

### Master Playbook

To group up the functions we want, we'll use a master playbook at the top of our folder structure:
```
directory/
├── inventory.ini
├── dorian.yml
└── roles/
    ├── glusterfs/
    │   ├── tasks/
    │   │   ├── install.yml
    │   │   └── main.yml
    ├── docker/
    │   ...
    ├── swarm/
    │   ...
```
Here dorian.yml is the master playbook

Starting and testing everything:
```
ansible-playbook -i inventory.ini dorian.yml
```

# N.A.D.I.R

# Grafana

# Swarm

# Portainer

# CloudFlare

# GlusterFS
