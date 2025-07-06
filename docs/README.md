The docs here will serve both as the project specific documentation and as a knowledge-base for us
There will be key-configuration steps on used tools, as well as explanations of how they work, why we use them, etc.

# Our Approach (extended)

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

## TTICHAN GraSP CloPAG
(Yes, that is how we will refer to this project from now on)
### Project Summary

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

# Doc Structure

```
├── 0_INTRODUCTION
│   ├── ARCHITECTURE.md
│   └── PROJECT_OVERVIEW.md
├── 1_INFRASTRUCTURE
│   ├── CLAVISTER_FW.md
│   ├── GLUSTERFS_STORAGE.md
│   ├── HARDWARE.md
│   └── NETWORK.md
├── 2_DEPLOYMENT
│   ├── ANSIBLE.md
│   ├── PORTAINER.md
│   ├── SERVICES.md
│   ├── SWARM.md
│   └── TRAEFFIK_PANGOLIN.md
├── 3_SECURITY_AND_AUTH
│   ├── AUTHENTIK_SSO.md
│   ├── CLOUDFLARE.md
│   └── HARDENING.md
├── 4_MONITORING_LOGGING
│   ├── GRAFANA.md
│   ├── INFLUXDB.md
│   ├── NADIR.md
│   └── TOM_AGENTS.md
├── 5_BCP_AND_BRP
│   ├── BCP
│   │   ├── CONTAINER_CONTROL.md
│   │   ├── METRIC_MONITORING.md
│   │   ├── OVERVIEW.md
│   │   └── PORTAINER.md
│   └── BRP
│       ├── CLEAN_REDEPLOYMENT.md
│       ├── HUGO_BACKUPS.md
│       ├── OVERVIEW.md
│       └── RECOVERY_WORKFLOW.md
├── 6_MAINTENANCE
│   ├── FIXES.md
│   └── UPGRADES.md
├── 7_REFERENCES
│   ├── ACRONYMS_AND_TERMS.md
│   ├── EXTERNAL_RESOURCES.md
│   └── LICENSE.md
└── README.md
```
