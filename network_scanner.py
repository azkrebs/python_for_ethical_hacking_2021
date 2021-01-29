#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments(): #uses parser inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP Range") #if argument entered incorrectly, error will pop up with help
    #first two strings tell what acceptable input and third string = to dest is setting destination for the input
    options = parser.parse_args()
    if not options.target: #checking if input is correct
        parser.error("[-] Please specify target IP / IP Range, use --help for more info.") #error statement
    return options

def scan(ip): #function that scans entire network
    arp_request = scapy.ARP(pdst=ip) #looking for ip
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #looking for mac address
    arp_request_broadcast = broadcast/arp_request #combining two variables into one packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #creating list of results

    print("IP\t\t\tMAC Address\n------------------------------------------")
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list): #just a function for printing result
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

options = get_arguments() #creating new variable options for scan_result
scan_result = scan(options.target) #creating new variable scan_result that is equal to a scan of all the options
print_result(scan_result) #calling print_result to print scan_results for results to be displayed as outputs
