Considering uploading a file:

    1. Chunks for the file is created and the root hash will also be created.
    2. Send request to the tracker server with file name and the root hash value.
        Data format: <<<kind>>>?file_name|root_hash
    3. Tracker saves both of the information.
    4. Uploader gets a success message from the tracker.
    5. Uploader again sends request to the tracker to get the list of the peers in the network.
    6. Uploader gets the list of peers in the network.
    7. Sends the chunks also the meta information about the chunk.
    8. Peers in the network receive the chunks and store the chunks and also the meta data along with it.

Start tracker server:
`docker run -it --rm -v "/home/kabilan/Desktop/Semester8/CS4262 - Distributed Systems/Project/Implementation/tracker":/app -p 8080:12345 tracker /bin/bash`
`python3 server.py`

Start peer server:
`docker run -it --rm -v "/home/kabilan/Desktop/Semester8/CS4262 - Distributed Systems/Project/Implementation":/app -p 8081:12345 tracker /bin/bash`
`python3 server.py`

`docker run -it --rm -v "/home/kabilan/Desktop/Semester8/CS4262 - Distributed Systems/Project/Implementation":/app -p 8082:12345 tracker /bin/bash`
`python3 server.py`

`docker run -it --rm -v "/home/kabilan/Desktop/Semester8/CS4262 - Distributed Systems/Project/Implementation":/app -p 8083:12345 tracker /bin/bash`
`python3 server.py`

`docker run --rm -p 8080:12345 sdss python3 tracker/server.py`
`docker run --rm -p 8081:12345 sdss python3 server.py`
`docker build -t sdss:latest .`
