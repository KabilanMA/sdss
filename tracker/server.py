import socket
import threading
import os
import json
import pickle
from database import Database

database = Database()


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def handle_client(client_socket: socket.socket, client_address):
    # data from client
    try:
        client_ip = client_address[0]
        full_data: str = client_socket.recv(2048).decode()
        global database
        temp = [a.strip() for a in full_data.split("?")]
        if (len(temp)!=2):
            response = "Invalid Input Format"
        kind = temp[0]
        data = temp[1]

        if (kind=="upload"):
            file_name, root_hash, file_size, chunk_count = data.split("|")
            db_data = database.upload_file(file_name, file_size, root_hash, chunk_count)
            client_socket.sendall(str(db_data[0]).encode())
        elif(kind=="fetch"):
            # fetch file names for view
            file_names = database.fetch_all_filename()
            output_names = dict()
            for i, name in enumerate(file_names):
                output_names[i] = [name[0], name[1]]
            client_socket.sendall(json.dumps(output_names).encode())
        elif(kind=="peer"):
            # update peers for the file
            file_id, peer_ip, peer_port = data.split('|')
            database.update_file_peer(file_id, peer_ip, peer_port)
            client_socket.send("Success".encode())
        elif(kind=="download"):
            file_name, _ = data.split('|')
            rows, root_hash, chunk_count = database.get_file_info(file_name)
            rows.append(root_hash)
            rows.append(chunk_count)
            client_socket.send(json.dumps(rows).encode())
        
    finally:
        # close the connection
        client_socket.close()

def server():
    host = '0.0.0.0'  # all available interfaces
    port = 12345 

    # server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Tracker is listening on {host}:{port}")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")
        create_folder_if_not_exists("./tracker/data")

        # Handle client request in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address,))
        client_handler.start()

# Start the server
server_thread = threading.Thread(target=server)
server_thread.start()
