# IntegrityVault - A Secure Distributed Storage System

IntegrityVault is a secure distributed storage system that distributes file partitions as chunks across a distributed network. While ensuring data integrity, this system operates without incorporating fault tolerance mechanisms. IntegrityVault satisfies three basic requirements: it ensures the random distribution of file chunks among cluster nodes for security, allowing users to seamlessly retrieve and reconstruct the entire file at any time; it guarantees data integrity and validation by enabling verification of file chunks to confirm they have not been tampered with, using techniques such as a Merkle Tree; and it provides a user-friendly interface that allows users to list and search for stored files, view file metadata (including file name, size, date of storage, type, etc.), verify file integrity, download files, and upload new files to the distributed storage system.

A Merkle tree, is a data structure used in cryptography and computer science to ensure data integrity and efficiency. It is a binary tree in which every leaf node contains a hash of a data block, and each non-leaf node contains a hash of its child nodes. This hierarchical arrangement allows for quick and efficient verification of data integrity.

## How to run the application

1. Setup the enviroment with docker containers.

1.1 Use the following command to create docker image to run the containers.

`docker build -t sdss .`

1.2 Assume we need one tracker server and three worker storage nodes, therefore we need to create 4 containers.

Use the following command in 4 terminals to start 4 continers to run with previously created docker image.

`docker run -it --rm -v "/local/path/to/the/project/directory":/app -p 8080:12345 sdss /bin/bash`

2. Run the servers

Inside the container's interactive terminal, run the servers.

For tracker server: `python3 tracker/server.py`

For worker storage nodes: `python3 server.py ./data_x`
(replace `x` with different numbers for each container to have differnt volume mount)

Now all servers are running succesfully.

3. Upload file

Run the following command to open UI client to upload and download files.

`python3 ui/gui.py`

Now user should be able to upload and download anyfiles.
