JMS is a Bastion and PAM open-source tool

# Definition of Terms
## Asset

An asset is a resource you want to access: a VM, a website, a MariaDB database, a network device (firewall, router, etc.).
An asset mainly consists of:

- A name
- A hostname or IP address
- An operating system (OS)
- One or more accounts (see "Account") associated with it for connection
- One or more nodes (see "Node") associated for organizational purposes

Example: I want to access the database of "Vanta Medical" (a fictional company) from the bastion.
I select the creation of an asset of type "database", then choose "mariadb".
I name it "vantamedical-mariadb", with "address" as 192.168.122.235.
I select the node where it will be located, here: DEFAULT/PrestaVANTAMEDICAL/DATABASES.

## Account

An account allows you to connect to an asset.
Example: I have an asset called "vantamedical-mariadb", which is a MariaDB database for the company Vanta Medical. The database is accessible via the "dorian" account, so that is the account we add and "push" to the asset.

## Node

A node is essentially a folder that contains one or more assets.
Each node has its own permissions and privileges depending on the groups (see "Group") that are authorized to access it.
