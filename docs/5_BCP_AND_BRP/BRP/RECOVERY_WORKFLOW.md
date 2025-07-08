# Summary

Our recovery workflow is here to help us with our BRP in case of a problem

# Workflow

Check which hosts on the Dell FX2S are down and which GlusterFS bricks need restoring.
Connect to the remote VPS where backups are stored and make sure the latest backups are good.
Restore the backed-up GlusterFS bricks from the VPS to the affected hosts.
Verify the data is consistent and the hosts are back online in the cluster.
Ensure everything works smoothly again.

## If the FX2S is down

The VPS is used to decompress the latest backup and run the infrastructure in a single-node environment
