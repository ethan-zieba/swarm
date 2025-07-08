# Summary

N.A.D.I.R is a lightweight log ingestion server that receives and processes log lines sent via HTTP, parsing them into structured data points with tags and fields. 
N.A.D.I.R enriches logs by analyzing messages for sensitive commands (detailed in the `touchy.yml` config file), assigning alert levels and titles to help identify potential security events. 
These processed logs are then written into an InfluxDB time-series database for storage and later visualization in our Grafana.

# Configuration

`touchy.yml` must be placed in the same directory as N.A.D.I.R's `main.py`

`touchy.yml` default contents snippet:
```
touchy_commands:
  - command: rm -rf
    level: 5
    alert_title: "Dangerous remove ?"

  - command: sudo
    level: 4
    alert_title: "sudo command, privesc?"

  - command: crontab
    level: 4
    alert_title: "persistence tweak"

  - command: passwd
    level: 3
    alert_title: "creds change attempt"
```
