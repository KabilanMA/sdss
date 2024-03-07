import socket
import threading
import json

from internal.filestorage import chunk

def handle_client(client_socket):
     # Receive data from client
    data = client_socket.recv(2048).decode()
    # print("Received from client:", data)

    decoded_data = json.loads(data)
    kind = decoded_data['kind']
    if (kind == "upload"):
        file_name = str(decoded_data['file_id']) + "_" + str(decoded_data['chunk_id']) + "_" + str(decoded_data['root_hash']) + ".json"
        with open(file_name, "wb") as file:
            file.write(json.dumps(decoded_data).encode())
    # Send response back to client
    response = "Success"
    client_socket.send(response.encode())

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

    print(f"Server is listening on {host}:{port}")

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connected to {client_address}")

        # Handle client request in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Start the server
server_thread = threading.Thread(target=server)
server_thread.start()
