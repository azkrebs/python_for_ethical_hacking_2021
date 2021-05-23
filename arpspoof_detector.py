#!/usr/bin/env python
import scapy.all as scapy

def get_mac(ip): #Simply extracts mac address
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request #the slash combines the two into a single variable
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_pack)

def process_sniffed_pack(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwrc

            if real_mac != response_mac:
                print("[+] You are under attack -- ARP Spoof")
        except IndexError:
            pass


sniff("eth0")