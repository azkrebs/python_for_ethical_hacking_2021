#!/usr/bin/env python

import requests

target_url = "http://10.0.2.5/dvwa/login.php"
data_dict = {"username": "admin", "password": "password", "Login": "submit"}  # all values required to successfully login
response = requests.post(target_url, data=data_dict)  # sending request (post type) with data containg all required values
print(response.content)