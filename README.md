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
