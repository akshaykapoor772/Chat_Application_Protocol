#Sever side for chat protocol
from multiprocessing.connection import Client
import selectors
import socket
import sys
from threading import Thread

def allow(client, addr):
    #Manages incoming clients processes
    client, dest = client.accept() # Accept a connection
    print(f'{dest} is connected') # Print the connection address
    client.setblocking(False) # Set connection to non-blocking
    chos.register(client, selectors.EVENT_READ, stateful) # Register the connection on the selector

def stateful(client, addr):
    #Checks the states, then processes and sends the appropriate message
    data = client.recv(1024).decode("utf8") # Receive data with utf8 decoding
    temp1, temp2, msg = data.splitlines() # Split the data into 3 parts
    mean, dest, ver = temp1.split(':') # Split the first line into 3 parts

    if mean == '0001': # If the message is a connection request
        auth(client, temp2, dest) # Authenticate the user
    if mean == '0010': # If the message is a message
        sendall(client, msg) # Send the message to all users
    if mean == '0011': #Tells which new user is connected
        sendnew(client, msg) # Send the message to all users
    if mean == '0100': # If the message is a disconnection request
        close(client, msg) # Close the connection
    else:
        pass

def auth(client, idpass, dest): #Authenticates the user
    id, seckey = idpass.split(':') # Split the id and password

    try:
        if IDPASS[id] == seckey: # If the id and password match
            current = 331 # Set the current state to 331
            keyword = 'User checked and verified' 
            print(f'{current}:{keyword} -> {id} has been verified') 
            connectedusers[client] = dest # Add the client to the connected users
        else:
            current = 231 # Set the current state to 231
            keyword = 'User not verified' 
    except KeyError:
        current = 231
        keyword = 'User not verified'
    
    temp1 = VER + ':' + str(current) + ':' + keyword + '\r\n' # Create the packet
    temp2 = id +'\r\n' # Add the id to the packet
    msg = 'na' # Add the message to the packet
    finpkt = temp1 + temp2 + msg # Create the final packet
    client.send(bytes(finpkt, "utf8")) # Send the packet with utf8 encoding

def sendnew(client, msg): #Sends the message to all users tellings which new user is connected
    current = '251' # Set the current state to 251
    keyword = 'New connection' 
    id = connectedusers[client] # Get the id of the user
    temp1 = VER + ':' + str(current) + ':' + keyword + '\r\n' # Create the packet
    temp2 = id +'\r\n' # Add the id to the packet
    finpkt = temp1 + temp2 + msg # Create the final packet

    while True:
        try:
            for c in connectedusers: # Send the packet to all users
                c.send(bytes(finpkt, "utf8"))
            break
        except BlockingIOError: # If the socket is blocked, continue
            continue

def sendall(client, msg): #Sends the message to all users
    current = '250'
    keyword = 'All users'
    id = connectedusers[client] 
    temp1 = VER + ':' + str(current) + ':' + keyword + '\r\n'
    temp2 = id +'\r\n'
    finpkt = temp1 + temp2 + msg # Create the final packet

    while True:
        try:
            for c in connectedusers: # Send the packet to all users
                    c.send(bytes(finpkt, 'utf8')) # Send the packet with utf8 encoding
            break
        except BlockingIOError:
            continue

def close(client, msg): #Closes the connection and removes the user from the connected users
    current = '253'
    keyword = 'User disconnected'
    id = connectedusers[client] 
    temp1 = VER + ':' + str(current) + ':' + keyword + '\r\n' 
    temp2 = id +'\r\n'
    finpkt = temp1 + temp2 + msg

    client.close() # Close the client socket
    del connectedusers[client] # Remove the client from the connected users
    chos.unregister(client) # Unregister the client from the selector
    while True: 
        try:
            for c in connectedusers:
                c.send(bytes(finpkt, "utf8")) # Send the packet to all users telling which user has disconnected
            break
        except BlockingIOError:
            continue

IDPASS = {'Akshay': 'qwerty',
                  'John': 'password',
                  'Sara': '12345'} # Dictionary of id and password

connectedusers = {} # Dictionary of connected users

HOST='' # Hostname of the server (empty becuase running on same machine)
PORT = 8080 # Port number of the server
DEST = (HOST, PORT) # Address of the server
VER=f'{1}' # Version of the protocol

try:
    running = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
except socket.error: # If the socket cannot be created
    print('Failed to create socket') # Print error message
    sys.exit(1) # Exit the program

running.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set the socket to reuse the address
running.setblocking(False) # Set the socket to non-blocking
running.bind((HOST, PORT)) # Bind the socket to the address
running.listen() # Listen for connections
print(f'Listening on port: {PORT}') # Print the port number

isrunning = True # Set the server to running
chos = selectors.DefaultSelector() # Create a selector object
chos.register(running, selectors.EVENT_READ, allow) # Register the server socket on the selector

while isrunning: # While the server is running
    for a, b in chos.select(timeout=1): # Select the events
        callback = a.data # Get the callback
        callback(a.fileobj, b) # Call the callback
