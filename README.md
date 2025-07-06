# Docker Swarm
## Project for La Plateforme_
*but mostly for ourselves at this point*

### Original Statement

Deploy a full Docker Swarm cluster with an NFS storage, using 4 VMs (3 for the Swarm, 1 for the NFS). Deploy services such as a local repository, a MariaDB, a PHP environment, an Nginx and a VSCode Server.

### Our Approach

We pushed the project towards a big, production ready, reliable, scalable, robust environment.
Please read [our documentation](https://github.com/ethan-zieba/swarm/blob/docs/docs/README.md) for further understanding of our approach

# Getting Started

1. Install a basic Debian 12 on each host
2. Create an "ansible" user on cyril, and a "management" user on the other hosts, all with passwordless sudo
3. Create an ssh ed25519 keypair for ansible@cyril, push its public key on the other hosts management account
4. Install ansible and ansible posix on cyril [using pipx and ansible-galaxy](https://github.com/ethan-zieba/swarm/blob/docs/docs/2_DEPLOYMENT/ANSIBLE.md#installing-ansible)
5. Further instructions to come... (a script is in the making)

# Stack Progress

## Overall Progress
**T**TI**C**H**A**N Gra**SP** ClAG
**54%**
┌──────────────────────────────────────────────────┐  
|███████████████████████████░░░░░░░░░░░░░░░░░░░░░░░|
└──────────────────────────────────────────────────┘
## Detailed Progress

| Component                      | Status             | Progress               |
|-------------------------------|--------------------|------------------------|
| Clavister (Firewall)           | Deployed           | ███████████████████ (100%) |
| Traefik (Reverse Proxy)        | Deployed           | ███████████████████ (100%) |
| Swarm (Docker Orchestration)   | Deployed           | ███████████████████ (100%) |
| Ansible (Provisioning)         | Deployed           | ███████████████████ (100%) |
| Portainer (Swarm UI)           | Deployed           | ███████████████████ (100%) |
| GlusterFS (Distributed Storage)| Deployed           | ███████████████████ (100%) |
| N.A.D.I.R (Intrusion Detection)| Planning/Starting  | ███████▁▁▁▁▁▁▁▁▁▁▁▁ (35%)     |
| InfluxDB (Time-series DB)      | In Progress        | █████▁▁▁▁▁▁▁▁▁▁▁▁▁▁ (25%)     |
| Grafana (Visualization)        | In Progress        | ███▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ (15%)     |
| T.O.M (Telemetry Agent)         | In Progress       | ███▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ (15%)     |
| H.U.G.O (Offsite Storage)       | In Progress       | ██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁ (10%)     |
| Cloudflare Tunnel              | Not Deployed       | ░░░░░░░░░░░░░░░░░░░ (0%)      |
| Authentik (SSO)                | Not Deployed       | ░░░░░░░░░░░░░░░░░░░ (0%)      |

