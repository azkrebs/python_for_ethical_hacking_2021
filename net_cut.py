#!/usr/bin/env python
#module to interact with queue

import netfilterqueue

def process_packet(packet):
    print(packet)
    packet.drop()#cuts internet connection of client by not allowing packets to reach destination

queue = netfilterqueue.NetfilterQueue() #creating instance of netfilterqueue object and placing it in variable named "queue"
queue.bind(0, process_packet) #connecting object to queue we created in terminal using same id we gave in the terminal
#have callback function to execute one each packet that will be caught in queue
queue.run() #runs the queue we created

