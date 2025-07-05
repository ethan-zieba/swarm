# Docker Swarm
## Project for La Plateforme_
*but mostly for me at this point*

*Please note that the use of the first person in the documentation for this project means, in fact, both my associate and I. 

### Original Statement

Deploy a full Docker Swarm cluster with an NFS storage, using 4 VMs (3 for the Swarm, 1 for the NFS). Deploy services such as a local repository, a MariaDB, a PHP environment, an Nginx and a VSCode Server.

### Our Approach

We are using this as an opportunity to dig deeper into building secure and resilient physical infrastructures.

For the proof of concept (PoC), we ran a 4-node Raspberry Pi 4 cluster. The first production-ready deployment uses a **DELL FX2S** chassis with four blades as well as an **Arista 720XP** for the connectivity.

Storage will be made resilient by replicating and distributing it across three hosts using **GlusterFS**.

To make services and management interfaces accessible remotely, we will set up a **Pangolin** reverse proxy (instead of **NGINX** – mainly to try something new), paired with a **Cloudflare tunnel** to protect against DDoS attacks and to hide our home IP.

For logs and metrics, we will build a custom log aggregator called **N.A.D.I.R,** which will index into **InfluxDB** and be visualised using **Grafana**. Logs will be gathered by lightweight agents named **T.O.M**.

**For the BRP (Business Restarting Plan)**: 
- We will create custom backup tooling – named H.U.G.O
- Full infrastructure should be redeployable on new hardware, using Ansible for provisioning and updates

**For the BCP (Business Continuity Plan)**:
- We will monitor key metrics like CPU, memory, and disk usage via T.O.M-managed probes
- Container and services management will be handled using **Portainer**

**For the Infrastructure Security, Load Balancing and Identities**

- Perimeter will be protected by a Clavister E10 Firewall, filtering traffic by source, protocol, port, etc.
- Authentik will serve as the central SSO for user authentication
- We will use Traefik to balance traffic across all nodes and ensure smooth integration with Pangolin and the deployed services

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
