import socket
import threading

from internal.filestorage import chunk
from internal.filestorage.merkletree import MerkleTree
from config_info import *

def update_tracker(data):
    ip = tracker_ip
    port = tracker_port
    client(data, ip, port)

def upload(file_path):
    chunks = chunk.chunk_file(file_path)
    tree = MerkleTree()
    root_hash = tree.get_root_hash(chunks)
    tracker_data = "upload?" + file_path + "|" + root_hash
    update_tracker(tracker_data)

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