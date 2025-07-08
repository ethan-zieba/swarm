# Summary

T.O.M agents are partly configurable lightweight logging agents running as a service
They send logs to a N.A.D.I.R endpoint
For now they are able to monitor one log file at once but there are more features to come

# Configuration

`tom_config.yml` file must be placed in the same directory as the python script

```tom_config.yml
nadir_endpoint: "http://192.168.1.1:3100/nadir/api/v1/push"
hostname: "walid"
log_file: "/home/management/.bash_history"
```

To append commands to the .bash_history in realtime, change the env variable: `PROMPT_COMMAND='history -a'`
