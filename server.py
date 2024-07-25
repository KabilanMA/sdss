import socket
import threading
import json
from datetime import datetime
import os
import time
import argparse

from internal.filestorage import chunk
from utils.file import create_folder_if_not_exists

from config_info import *

def get_chunks(file_id : str, data_directory : str):
    # Iterate through the files in the directory
    chunks = []
    chunk_ids = []
    folder_path = data_directory
    for filename in os.listdir(folder_path):
        if filename.startswith(file_id+"_") and not (filename.endswith(".json")):
            file_path = os.path.join(folder_path, filename)
            json_file_path = file_path+".json"
            data_dict = dict()
            with open(json_file_path, "r") as json_file:
                data_dict = json.load(json_file)
            chunk_id = data_dict['chunk_id']
            chunk_ids.append(chunk_id)
            with open(file_path, "rb") as file:
                byte_data = file.read()
                chunks.append(byte_data)
    
    return chunks, chunk_ids

def handle_client(client_socket: socket.socket, client_address, data_directory):
     # Receive data from client
    create_folder_if_not_exists(data_directory)
    global file_name_global
    data = json.loads(client_socket.recv(1024*16).decode())
    if data['kind'] == "upload":
        data['uploader'] = client_address
        data['timestamp'] = str(datetime.now())
        file_name = str(data['file_id']) + "_" + data['root_hash'] + ".part_" + str(data['chunk_id'])
        data['file_name'] = file_name
        file_name_ext = file_name + ".json"
        with open(data_directory+"/"+file_name_ext, "w") as file:
            file.write(json.dumps(data))
        response = dict()
        response['type'] = "upload"
        response['type_section'] = "metadata"
        response['success'] = True
        response['file_name'] = file_name_ext
        client_socket.sendall(json.dumps(response).encode())

        received_data = b''
        while True:
            chunk = client_socket.recv(chunk_size)
            if not chunk:
                break
            received_data += chunk
        with open(data_directory+"/"+file_name, 'wb') as chunk_file:
            chunk_file.write(received_data)

    elif (data['kind'] == "download"):
        file_id = data['file_id']
        chunks, chunk_ids = get_chunks(str(file_id), data_directory)
        client_socket.sendall(str(len(chunks)).zfill(128).encode())
        for i in range(len(chunks)):
            client_socket.sendall(str(chunk_ids[i]).zfill(128).encode())
            print("sending chunks")
            client_socket.sendall(chunks[i])
            time.sleep(1)
            print(len(chunks[i]))

    client_socket.close()

def server(data_directory):
    # Define host and port for the server
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345      # port number

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is listening on {host}:{port}")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Handle client request in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, data_directory))
        client_handler.start()

parser = argparse.ArgumentParser(description="Argument parser to parse commandline argument for mount location")
parser.add_argument('data_directory', type=str, help="Location of the data directory")

args_ = parser.parse_args()


# Start the server
server_thread = threading.Thread(target=server, args=[args_.data_directory])
server_thread.start()
