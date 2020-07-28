import socket
import threading

PORT = 5000
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "Client Disconnected"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    '''
        Handle individual connection between client-server
        Will be running concurrently for each client
    '''
    # displays all the new connections to the server
    print(f"[NEW CONNECTIONS] {addr} connected.")
    connected = True
    while connected:
        # conn.recv() is a blocking line of code and hence you need threads for simultaneous connections
        # from other clients. The messages received are encoded and hence it has to be decoded at the server.
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # Check if you're getting a valid message
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))
    
    # Gracefully close the connection
    conn.close()


def start_socket():
    '''
        Listen and handles connections with clients
    '''
    # listen for new client connections
    server.listen()     
    print(f"[LISTENING] server is listening on {SERVER}")             
    # Infinite loop so that the server is always listening
    while True:
        # Waits for a new connection to the server.   
        # Server accepts the address of a client connection                    
        conn, addr = server.accept() 
                                     
        #Checks the number of active connections
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #Displays new thread for each of the new clients 
        # (threading.activeCount()-1 means there is always a thread running to listen to new connections)
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

print("[STARTING] server is starting...")
start_socket()