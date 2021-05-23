#!/usr/bin/env python

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "10.0.2.5/mutillidae/"

with open("/root/Downloads/subdomains.txt", "r") as wordlist_file:
    # can use "common-dirs.txt" to find directories or "subdomains.tx" to find hidden domains
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        # word + "." + target_url  for domains and target_url + "/" word for directories
        response = request(test_url)
        if response:
            print("[+] Subdomain discovered --> " + test_url)  # directories = URL, domains = subdomains
            # can add loop to continue searching for more hidden subdomains