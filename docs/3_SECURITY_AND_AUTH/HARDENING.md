# Tools
## Auditd
As the entrypoint for our infrastructure will be cyril, we install auditd on it: 

```
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd
```
Key configuration files

- `/etc/audit/auditd.conf` - main configuration file (log location, max log size...)
- `/etc/audit/rules.d/*.rules` - audit rules
- `/etc/audit/audit.rules` - loaded rules at runtime

Default log file location: `/var/log/audit/audit.log`
