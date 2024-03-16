import socket
import threading
import random
import json
import pickle
import os
import time

from internal.filestorage import chunk
from internal.filestorage.merkletree import MerkleTree
from config_info import *
from utils.file import extract_file_name, extract_file_size, create_folder_if_not_exists
from internal.filestorage.chunk import remove_padding

def update_tracker(data:str):
    ip = tracker_ip
    port = tracker_port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.sendall(data.encode())
    response = client_socket.recv(2048).decode()
    client_socket.close()
    return response

def fetch_file_names():
    data = "fetch?None|None"
    res = update_tracker(data)
    file_names = json.loads(res)
    return file_names

def distribute_2_peers(file_id, chunks: list[bytes], root_hash: str):
    peers_set = set()
    output = []
    for i, chunk in enumerate(chunks):
        peer_to_choose = random.randint(0, len(peers)-1)
        peer = peers[peer_to_choose]
        peer_ip = peer['ip']
        peer_port = peer['port']
        
        if(not(peer_ip in peers_set)):
            peers_set.add(peer_ip)
            output.append([peer_ip, peer_port])
            add_peer = True
        else:
            add_peer = False

        data = dict()
        data['kind'] = 'upload'
        data['file_id'] = file_id
        data['chunk_id'] = i
        data['root_hash'] = root_hash

        dump_data = json.dumps(data)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((peer_ip, peer_port))
        client_socket.sendall(dump_data.encode())

        response = json.loads(client_socket.recv(1024*16).decode())
        if response['success'] == True:
            client_socket.sendall(chunk)

        client_socket.close()

        if (add_peer):
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

def fetch_files_from_peers(file_id, total_chunk_count):
    chunks = ["0" for _ in range(total_chunk_count)]
    try:
        for peers in file_id:
            file_id_, peer_ip, peer_port = peers
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data = dict()
            data['kind'] = 'download'
            data['file_id'] = file_id_

            client_socket.connect((peer_ip, peer_port))
            client_socket.sendall(json.dumps(data).encode())

            response = client_socket.recv(128).decode()
            local_chunk_count = int(response)

            for i in range(local_chunk_count):
                response = client_socket.recv(128).decode()
                chunk_id = int(response)

                chunk_data = client_socket.recv(chunk_size)
                while len(chunk_data) < chunk_size:
                    more_data = client_socket.recv(chunk_size)
                    chunk_data += more_data
                if (chunks[chunk_id] == "0"):
                    chunks[chunk_id] = chunk_data
        return chunks
    except:
        return []
            

def download_file(file_name):
    data = "download?" + file_name + "|None"
    response = update_tracker(data)
    response_data = json.loads(response)
    original_root_hash = response_data[-2]
    chunks = fetch_files_from_peers(response_data[:-2], response_data[-1])
    tree = MerkleTree()
    if ((len(chunks) <= 0) or (not tree.validate_chunks(chunks, original_root_hash))):
        return False
    create_folder_if_not_exists('./downloads')
    chunk.create_file_from_chunks("./downloads/"+file_name, chunks)
    return True
    # chunk.create_file_from_byte("./downloads/"+file_name, chunks)

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
        response = client_socket.recv(chunk_size*5).decode()
    except UnicodeDecodeError:
        response = client_socket.recv(chunk_size+1024)

    # Close the connection
    client_socket.close()
    return response