import socket
import threading
import json
from datetime import datetime

from internal.filestorage import chunk
from utils.file import create_folder_if_not_exists

from config_info import *

file_name_global = ""

def handle_client(client_socket, client_address):
     # Receive data from client
    create_folder_if_not_exists('./data')
    global file_name_global
    response = "Not completed"
    data = client_socket.recv(chunk_size+1024)
    try:
        data = data.decode()
        if file_name_global == "":
            decoded_data = json.loads(data)
            kind = decoded_data['kind']
            if kind == "upload":
                decoded_data['uploader'] = client_address
                decoded_data['timestamp'] = str(datetime.now())
                file_name = str(decoded_data['file_id']) + "_" + decoded_data['root_hash'] + ".part_" + str(decoded_data['chunk_id'])
                decoded_data['file_name'] = file_name
                file_name_ext = file_name + ".json"
                # Convert bytes to JSON-serializable string
                decoded_data_str = json.dumps(decoded_data)
                with open("./data/"+file_name_ext, "w") as file:
                    file.write(decoded_data_str)
                    file_name_global = file_name
            response = "Successfully saved metadata"
        else:
            response = "Retry in a while"
    except UnicodeDecodeError:
        chunk_file_name = file_name_global
        with open("./data/"+chunk_file_name, 'wb') as chunk_file:
            chunk_file.write(data)
        
        file_name_global = ""
        response = "Successfully saved chunks"
    
    finally:
        print(response)
        client_socket.send(response.encode())
        # Close the connection
        client_socket.close()

def server():
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
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

# Start the server
server_thread = threading.Thread(target=server)
server_thread.start()
