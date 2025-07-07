As the entrypoint for our infrastructure will be cyril, we install auditd on it: 

```
sudo apt install auditd
sudo systemctl enable auditd
sudo systemctl start auditd
```
