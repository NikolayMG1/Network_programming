import socket

host = '127.0.0.1'
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

try:
    # Get number input from user
    user_input_number = input("Enter the number of threads: ")
    client_socket.send(user_input_number.encode('utf-8'))

    # Get graph input from user
    user_input_graph = input("Enter a graph as a dictionary: ")
    client_socket.send(user_input_graph.encode('utf-8'))

except ValueError:
    print("Invalid input.")

client_socket.close()
