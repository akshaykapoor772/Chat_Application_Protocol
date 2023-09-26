# Client side for chat protocol
from time import sleep
import time
import sys
import socket as skt
from threading import Thread
import tkinter

class Userinterface(tkinter.Frame): # Creates the user interface

    def __init__(self, master): 
        tkinter.Frame.__init__(self, master) 
        self.master = master 
        self.startwin() 
        self.rethr = Thread(target=self.stateful) # Creates a thread to receive messages continuously
        self.rethr.start() 

    def startwin(self): # Creates the start window to get login details
        self.master.geometry("500x400")
        self.master.title("Verify") 
        self.startlb = tkinter.Label(self.master, text="Enter ID and Password") 
        self.startlb.pack() # Creates the label to get login details
        self.userlb = tkinter.Label(self.master, text="ID") # Creates the label to get ID
        self.userlb.pack()

        self.user = tkinter.StringVar() # Creates the entry to get ID
        self.userent = tkinter.Entry(self.master, textvariable=self.user) 
        self.userent.pack() 

        self.passlb = tkinter.Label(self.master, text="Password") # Creates the label to get password
        self.passlb.pack()
        self.seckey = tkinter.StringVar()
        self.seckeyent = tkinter.Entry(self.master, textvariable=self.seckey)
        self.seckeyent.pack()

        self.check = tkinter.Button(self.master, text="Verify", command=self.verify) # Creates the button to verify
        self.check.pack()

        self.reply = tkinter.Label(self.master, text='') # Creates the label to display error messages
        self.reply.pack()

        self.datafr = tkinter.Frame(self.master) # Creates the frame to display messages
        self.bar = tkinter.Scrollbar(self.datafr) # Creates the scrollbar
        self.data = tkinter.Listbox(self.datafr, height=20, width=70,yscrollcommand=self.bar.set) # Creates the listbox

    def msgwin(self): # Creates the message window to chat once user is verified
        self.master.geometry("500x400")
        self.master.title("Group Chat")

        #Destroy items from start window
        self.check.destroy() 
        self.passlb.destroy()
        self.seckeyent.destroy()
        self.userent.destroy()
        self.userlb.destroy()
        self.startlb.destroy()
        self.reply.destroy()

        self.datafr = tkinter.Frame(self.master) # Creates the frame to display messages
        self.msg = tkinter.StringVar() # Creates the entry to get message
        self.msg.set('Type your message here') # Sets the default message
        self.bar = tkinter.Scrollbar(self.datafr) 
        self.data = tkinter.Listbox(self.datafr, height=20, width=70,yscrollcommand=self.bar.set)
        self.bar.pack(side=tkinter.RIGHT, fill=tkinter.Y) 
        self.data.pack(side=tkinter.LEFT, fill=tkinter.BOTH) 
        self.data.pack()
        self.datafr.pack()

        self.startfld = tkinter.Entry(self.master, textvariable=self.msg) # Creates the box to get message
        self.startfld.pack()

        self.exitbtn = tkinter.Button(self.master, text="Leave", command=self.quit) # Creates the button to leave
        self.exitbtn.pack()

    def verify(self): # Verifies the login details
        try:
            global ID # Global variable to store ID
            
            ID = self.user.get() # Gets the ID from the entry 
            seckey = self.seckey.get() # Gets the password from the entry
            body = 'na' # Body is not used in this case

            mean = '0001' # Message type
            dest = sock.ljust(32,' ') #32 bit space padded destination
            reln = mean + ':' + dest + ':' + VER + '\r\n' 

            temp1 = ID + ':' + seckey + '\r\n' # Creates the message to be sent
            fin = reln + temp1 + body # Creates the final packet
            client.send(bytes(fin, 'utf8')) # Sends the packet
            
            # Clears the entry
            self.seckey.set('') 
            self.user.set('') 

        except BrokenPipeError: # If the connection is broken
            pass

    def afterauth(self, head): # After authentication is successful show the message window and start receiving messages
        ID = head.split(':')[0] # Gets the ID from the header
        self.msgwin() # Shows the message window
        new = f'Hello {ID}' # Creates the greeting message to be sent to new user
        self.data.insert(tkinter.END, new) # Inserts the greeting message

        mean = '0011' # Message type
        dest = sock.ljust(32,' ') 
        reln = mean + ':' + dest + ':' + VER + '\r\n' 
        head = ID + '\r\n'
        msg = f'{ID} can start chatting now' 
        pkt = reln + head + msg
        client.send(bytes(pkt, 'utf8')) 

    def stateful(self): #STATEFUL (CHECKS THAT STATE IS CORRECT ACCORDING TO THE DFA)
        try:
            while True:
                pkt = client.recv(1024).decode('utf8') # Receives the packet
                currtemp, head, body = pkt.splitlines() # Splits the packet into header, body and current state
                curr = currtemp.split(':')[1] # Gets the current state from the header

                if curr == '250': 
                    self.data.insert(tkinter.END, body) # Inserts the message in the CHAT window
                if curr == '331': #verified successfully
                    self.afterauth(head) # Shows the message window and starts receiving messages
                if curr == '231': #if wrogn credentials
                    self.reply.config(text='Incorrect ID or Password') # Displays the error message
                if curr == '251': #Show greeting message and start sending and receiving messages
                    self.data.insert(tkinter.END, body) # Inserts the message in the CHAT window
                    self.startfld.bind('<Return>', self.sendmsg) # Binds the enter key to the send message function
        except ValueError: 
            pass

    def sendmsg(self, occur): # Sends the message to the server
        data = self.msg.get() # Gets the message from the entry
        data = ID + ':' + data  # Adds the ID to the message
        self.msg.set('') # Clears the entry

        mean = '0010' # Message type with padding
        dest = sock.ljust(32,' ') #32 bit space padded destination
        reln = mean + ':' + dest + ':' + VER + '\r\n' 
        head = ' ' + '\r\n'
        pkt = reln + head + data
        client.send(bytes(pkt, 'utf8')) # Sends the packet

    def quit(self): # Closes the connection and exits the program
        mean = '0100'
        dest = sock.ljust(32,' ')
        reln = mean + ':' + dest + ':' + VER + '\r\n'
        head = ID + '\r\n'
        msg = f'{ID} has left'
        pkt = reln + head + msg
        client.send(bytes(pkt, 'utf8'))
        self.startfld.destroy() # Destroys the entry
        self.close() # Closes the window
        self.destroy() # Destroys the window
        self.exitbtn.destroy() # Destroys the exit button


if __name__ == '__main__': 
    
    HOST = '172.16.10.19' # IP address of the server(Check your machine IP address with typing "ipconfig" command on cmd and enter the displayed IPv4 address here)
    PORT = 8080 # Port number on which server is running
    VER='0001' # Version number with padding
    ID='' 

    while True: 
        try:
            client = skt.socket(skt.AF_INET, skt.SOCK_STREAM) # Creates the socket
            client.connect((HOST, PORT)) # Connects to the server
            break # Breaks the loop if connection is successful
        except skt.error: # If the connection is not successful
            print('Error occured...Please check HOST address and PORT number are correct') # Displays the error message
            time.sleep(1) # Waits for 1 second

    host, port = client.getsockname() # Gets the host and port number of the client
    sock = (str(host)+'..'+str(port)) # Converts the host and port number to a string
    print(f'Socket address is {sock}') # Displays the socket address

    run = Userinterface(tkinter.Tk()) # Creates the window
    run.mainloop() # Runs the window