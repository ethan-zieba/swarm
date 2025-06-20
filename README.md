# Docker Swarm
## Project for La Plateforme_
*but mostly for me at this point*

*Please note that the use of the first person in the documentation for this project means, in fact, both my associate and I. 

### Original Statement

Deploy a full Docker Swarm cluster with an NFS storage, using 4 VMs (3 for the Swarm, 1 for the NFS). Deploy services such as a local repository, a MariaDB, a PHP environment, an Nginx and a VSCode Server.

### My Statement

_I want_ to further learn how to build secure, resilient physical infrastructures. For the proof of concept (PoC) I will use a 4 Raspberry Pi 4's cluster and a **DELL FX2S** chassis with 4 blades for the first production-ready version. 

_I need_ the storage to be resilient, so I will make it replicated and distributed over 3 hosts using **GlusterFS**. 

_I need_ my services and management interfaces to be accessible from abroad, so I will mount a **Pangolin** reverse proxy (I could mount an **NGINX** one, but I want to try **Pangolin** as I'm not familiar with the product and it looks fairly new), with a **CloudFlare tunnel** for anti-DDoS and hiding my home IP address. 

_I need_ to centralize important logs and metrics, so I will develop my own log gatherer called **N.A.D.I.R**, which will index data into an **InfluxDB**, and visualize it with a **Grafana**. The logs will be collected from custom microagents named **T.O.M**.

**For the BRP (Business Restarting Plan)**: 
- _I need_ to have backups, I will use a custom solution: **H.U.G.O**
- _I need_ to enable easy migration and re-installation of the entire infrastructure on clean, new, working hardware if needed, using **Ansible** for provisionning and updates.

**For the BCP (Business Continuity Plan)**:
- _I need_ to monitor critical metrics, such as memory/CPU load and disk space, using **T.O.M** managed probes.
- _I need_ to maintain tight control over services and containers running on the infrastructure, that's why I will use **Portainer**

_I need_ the infrastructure to be secure, I will setup a **Clavister E10 Firewall** filtering packets based on source location, protocol, port... 

_I need_ to manage logins easily, I will deploy an SSO solution called **Authentik** 

_I need_ the load to be perfectly balanced between nodes, and to enable **Pangolin** to access all of the hosts and services seamlessly. I will use Traeffik that integrates well with it

* * *

# TTICHAN GraSP CloPAG
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
- Pangolin - Modern Reverse Proxy product for homelabs and pre-prod environments
- Authentik - Simple SSO
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

## Key Concepts

**Services** run "on" the whole cluster, in the form of tasks executed by the hosts
**Networks** can be overlayed, so that a service can access the whole swarm infrastructure

# Portainer

Management interface for orchestrators such as Docker Swarm

# CloudFlare

# Pangolin

# Authentik

# GlusterFS

## Key concepts

Volumes are logical units made of bricks (on each host)

### Clients

#### FUSE
*Filesystem in Userspace*

Widely used client for GlusterFS, used to mount a volume and interact with it like a normal local filesystem, handling network communication transparently
Example: `mount -t glusterfs Walid:/gv0 /mnt/gv0`
The filesystem will be mounted in the user space instead of the kernel space

#### Other clients

GlusterFS could also be exported as NFS, simpler but slower and legacy
Or be used with gfapi/gogfapi (packages wrapping the api of the same name: gfapi)

### Summary

| **Concept**              | **Description**                                                                 |
|--------------------------|----------------------------------------------------------------------------------|
| **Type**                 | Distributed, scalable network filesystem                                        |
| **Architecture**         | Peer-to-peer, no centralized metadata server (fully decentralized)              |
| **Components**           | - **Brick**: Basic storage unit (a directory on a server)<br>- **Volume**: Logical collection of bricks |
| **Transport**            | Uses TCP (default port: 24007+) or optionally TLS                              |
| **Nodes (Peers)**        | The servers working together in the cluster. No central controller – fully equal.|
| **Volume Types**         | - **Distributed**: Spread data across bricks<br>- **Replicated**: Copy data to multiple bricks<br>- **Striped**: Striping across bricks<br>- **Dispersed**: Erasure-coded storage |
| **Scalability**          | Add more nodes/bricks to scale out horizontally                                |
| **High Availability**    | Achieved via replicated/dispersed volumes and client-side failover              |
| **Self-healing**         | Detects and syncs out-of-date or missing files across replicas                 |
| **No Metadata Server**   | Metadata is distributed; avoids single point of failure                         |
| **Management Tools**     | CLI (`gluster`), REST API (optional), and Ansible modules                      |
| **Security**             | IP-based access control, optional TLS encryption, file-level permissions       |

## Key configuration final steps

**We encountered probing errors as our /etc/hosts file was not properly set up**

Manually creating a volume:
```
gluster volume create gv0 replica 3 \
walid:/gluster/brick1 \
swagpi1:/gluster/brick1 \
swagpi2:/gluster/brick1
```

Checking for volume status and infos:
On any host:
```
gluster volume status
gluster volume info
gluster peer status
```

Checking for the daemon status:
`sudo systemctl status glusterd`

Checking for file replication:
`echo "hello from Walid" | sudo tee /mnt/gv0/test.txt`
Then:
`cat /mnt/gv0/test.txt` on another host
