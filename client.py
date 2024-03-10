import socket
import threading
import random
import json
import pickle
import os

from internal.filestorage import chunk
from internal.filestorage.merkletree import MerkleTree
from config_info import *
from utils.file import extract_file_name, extract_file_size


def fetch_file_names():
    data = "fetch?None|None"
    res = client(data, tracker_ip, tracker_port)
    file_names = json.loads(res)
    return file_names

def update_tracker(data):
    ip = tracker_ip
    port = tracker_port
    return client(data, ip, port)

def distribute_2_peers(file_id, chunks: list[bytes], root_hash: str):
    peers_set = set()
    output = []
    for i, chunk in enumerate(chunks):
        peer_to_choose = random.randint(0, len(peers)-1)
        peer = peers[peer_to_choose]
        peer_ip = peer['ip']
        peer_port = peer['port']

        if (peer_ip in peers_set):
            pass
        else:
            peers_set.add(peer_ip)
            output.append([peer_ip, peer_port])

        data = dict()
        data['kind'] = 'upload'
        data['file_id'] = file_id
        data['chunk_id'] = i
        data['root_hash'] = root_hash

        dump_data = json.dumps(data)
        client(dump_data, peer_ip, peer_port)
        client(chunk, peer_ip, peer_port)

        data = "peer?" + file_id + "|" + peer_ip + "|" + str(peer_port)
        update_tracker(data)
    return output

    
def upload(file_path):
    chunks = chunk.chunk_file(file_path)
    tree = MerkleTree()
    root_hash = tree.get_root_hash(chunks)
    tracker_data = "upload?" + extract_file_name(file_path) + "|" + root_hash + "|" + str(extract_file_size(file_path)) + "|" + str(len(chunks))
    file_id = update_tracker(tracker_data)

    peers = distribute_2_peers(file_id, chunks, root_hash)
    print(peers)

def fetch_files_from_peers(file_id):
    pass

def download_file(file_name):
    print(file_name)
    data = "download?" + file_name + "|None"
    response = update_tracker(data)
    fetch_files_from_peers(response['file_id'])
    print(json.loads(response))


def client(data, server_address, server_port):

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    # Send data to the server
    try:
        client_socket.send(data.encode())
    except AttributeError:
        client_socket.sendall(data)

    # Receive response from server
    try:
        response = client_socket.recv(chunk_size+1024).decode()
    except UnicodeDecodeError:
        response = client_socket.recv(chunk_size+1024)

    # Close the connection
    client_socket.close()
    return response