import socket
import ast
import threading
from queue import Queue
import time

def bfs(graph, start_node, result_queue):
    visited = set()
    queue = [start_node]
    visited.add(start_node)

    while queue:
        current_node = queue.pop(0)
        result_queue.put(current_node)

        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

def handle_client(client_socket):
    try:
        number_data = client_socket.recv(1024).decode('utf-8')
        if not number_data:
            return
        number_of_threads = int(number_data)
        print(f"Received number of threads from client: {number_of_threads}")

        graph_data = client_socket.recv(4096).decode('utf-8')
        print("Received graph data from client:")
        print(graph_data)  # Print the received graph data

        # Attempt to parse the received data
        graph_dict = ast.literal_eval(graph_data)
        print("Graph received:")
        for node, connections in graph_dict.items():
            print(f"{node}: {connections}")
            
        nodes = list(graph_dict.keys())
        nodes_per_thread = len(nodes) // number_of_threads

        threads = []
        result_queue = Queue()

        start_time = time.time()

        for i in range(number_of_threads):
            start_index = i * nodes_per_thread
            end_index = (i + 1) * nodes_per_thread if i < number_of_threads - 1 else len(nodes)
            subgraph = {node: graph_dict[node] for node in nodes[start_index:end_index]}
            print(subgraph)
            thread = threading.Thread(target=bfs, args=(subgraph, nodes[start_index], result_queue))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()

        while not result_queue.empty():
            print(f"BFS Result: {result_queue.get()}")

        print(f"Execution time with {number_of_threads} threads: {end_time - start_time} seconds")

    except ValueError:
        print("Received invalid data.")

    finally:
        client_socket.close()

host = '127.0.0.1'
port = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Server listening on {host}:{port}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established.")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
