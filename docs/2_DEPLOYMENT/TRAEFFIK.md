# Traefik
Reverse proxy that routes incoming requests to backend services based on configurable rules.

## Configuration Methods

### File Provider:
Routing rules are manually defined in configuration files. Any new service requires updating these files to add the corresponding routes. This method offers precise control but requires manual maintenance.

### Automatic Routing (Docker Provider):
Traefik runs inside Docker Swarm with the Docker provider enabled. It automatically discovers services labeled with routing information and updates routes dynamically, without manual configuration changes. This simplifies management but requires Traefik to have direct access to Docker or Swarm APIs.

## Summary

File provider = manual config, more control, less automation

Automatic routing = dynamic config via labels, less manual work, requires integration with Docker Swarm

For this project, we are using the File provider although we may change it in the near future
