import socket
import threading

def handle_client(client_socket):
    # Receive data from client
    data = client_socket.recv(1024).decode()
    print("Received from client:", data)

    # Send response back to client
    response = "Hello from server"
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

def client():
    # Define server address and port
    server_address = '127.0.0.1'  # Change to the other laptop's IP address or hostname
    server_port = 12345            # Change to the other laptop's port number

    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    # Send data to the server
    data = "Hello from client"
    client_socket.send(data.encode())

    # Receive response from server
    response = client_socket.recv(1024).decode()
    print("Received from server:", response)

    # Close the connection
    client_socket.close()

# Start server and client concurrently
server_thread = threading.Thread(target=server)
server_thread.start()

# Do other work while waiting for the server to start
# For example:
# time.sleep(10)

# Start client after the server has started
client()
