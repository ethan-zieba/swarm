### Summary

Gluster FS is a distributed, **scalable**, network filesystem
Metadata are decentralized, works in peer-to-peer

Volumes are logical units made of bricks (on each host)
Bricks are the basic storage units (typically a directory on a server)

GlusterFS uses TCP or TLS optionally

Upscaling a GlusterFS simply requires adding other nodes or bricks
The high availability is achieved via replicated/dispersed volumes

### Clients

#### FUSE
*Filesystem in Userspace*

Widely used client for GlusterFS, used to mount a volume and interact with it like a normal local filesystem, handling network communication transparently
Example: `mount -t glusterfs Walid:/gv0 /mnt/gv0`
The filesystem will be mounted in the user space instead of the kernel space

#### Other clients

GlusterFS could also be exported as NFS, simpler but slower and legacy
Or be used with gfapi/gogfapi (packages wrapping the api of the same name: gfapi)

### Installing/Configuring

**We encountered probing errors as our /etc/hosts file was not properly set up**

Manually creating a volume:
```
gluster volume create gv0 replica 3 \
walid:/gluster/brick1 \
ultrac1:/gluster/brick1 \
ultrac2:/gluster/brick1
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


### Securing/Troubleshooting

Securing the GFS cluster implies using a whitelist for the allowed hosts:
`gluster volume set myvolume auth.allow walid,ultrac1,ultrac2`

GlusterFS has **self-healing capabilities**:
`gluster volume heal myvolume info`
`gluster volume heal myvolume`
