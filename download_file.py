#!/usr/bin/env python

import requests

def download(url):
    get_response = requests.get(url)  # sends get request for URL that we passed and returns it to variable we made
    file_name = url.split("/")[-1]  # creating file name that is equal to last element of url
    with open(file_name, "wb") as out_file:  # creates a file in the working directory w/ a reference that helps us return to the file
        out_file.write(get_response.content)  # writes it in the file

download("https://hungarytoday.hu/wp-content/uploads/2018/02/18ps27.jpg")