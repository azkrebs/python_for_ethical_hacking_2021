#!/usr/bin/env python

import requests
import re
import urllib.parse as urlparse  # if wanting to use python 2 only import urlparse

target_url = "http://10.0.2.5/mutillidae/"
target_links = []


def extract_links_from(url):
    response = requests.get(url)  # submits get request and extracts it
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))  # regex searches html for a tags and returns it


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)  # calls itself making it a recursive method


crawl(target_url)
