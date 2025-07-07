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

We dearly present you...

# TTICHAN GraSP CloJKeG

TTICHAN GraSP CloPAG is a modular and resilient infrastructure project built around Docker Swarm
The goal is to design and operate a distributed containerized system that includes distributed storage, custom-built monitoring and logging pipeline, multiple security layers, with integrated BRP & BCP measures.

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
- Jumpserver - Bastion
- Keycloak - Simple SSO
- GlusterFS - Replicated and distributed storage
