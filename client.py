import socket
import threading
import random
import json

from internal.filestorage import chunk
from internal.filestorage.merkletree import MerkleTree
from config_info import *

def update_tracker(data):
    ip = tracker_ip
    port = tracker_port
    return client(data, ip, port)

def distribute_2_peers(file_id, chunks: list[bytes], root_hash: str):
    for i, chunk in enumerate(chunks):
        peer_to_choose = random.randint(0, len(peers)-1)
        peer = peers[peer_to_choose]
        peer_ip = peer['ip']
        peer_port = peer['port']
        data = dict()
        data['kind'] = "upload"
        data['file_id'] = file_id
        data['chunk_id'] = i
        data['root_hash'] = root_hash
        data['data'] = chunk.decode()
        dump_data = json.dumps(data)
        client(dump_data, peer_ip, peer_port)
    

def upload(file_path):
    chunks = chunk.chunk_file(file_path)
    tree = MerkleTree()
    root_hash = tree.get_root_hash(chunks)
    tracker_data = "upload?" + file_path + "|" + root_hash
    file_id = update_tracker(tracker_data)

    distribute_2_peers(file_id, chunks, root_hash)

def client(data, server_address, server_port):

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    # Send data to the server
    client_socket.send(data.encode())

    # Receive response from server
    response = client_socket.recv(1024).decode()
    print("Received from server:", response)

    # Close the connection
    client_socket.close()
    return response