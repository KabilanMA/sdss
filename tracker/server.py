import socket
import threading
import os
import json
from database import Database

database = Database()

def create_directory(dir_path="./data"):
    if not (os.path.exists(dir_path)):
        os.makedirs(dir_path)
        print(f"Directory '{dir_path}' created successfully")

def create_file(file_path="./data/test.json", data=""):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"JSON file '{file_path}' created successfully")

def handle_client(client_socket, client_address):
    # Receive data from client
    client_ip = client_address[0]
    full_data: str = client_socket.recv(1024).decode()
    global database
    temp = [a.strip() for a in full_data.split("?")]
    if (len(temp)!=2):
        response = "Invalid Input Format"
    kind = temp[0]
    data = temp[1]

    if (kind=="upload"):
        file_name, root_hash = data.split("|")
        db_data = database.upload_file(file_name, root_hash)

    print("Received from client:", data)

    # Send response back to client
    client_socket.send(str(db_data[0]).encode())

    # Close the connection
    client_socket.close()

def server():
    # Define host and port for the server
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 12345      # Choose a port number

    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    create_directory()

    print(f"Tracker is listening on {host}:{port}")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Handle client request in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address,))
        client_handler.start()

# Start the server
server_thread = threading.Thread(target=server)
server_thread.start()
