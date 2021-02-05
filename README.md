# python_for_ethical_hacking_2021
# commands to put in command prompt:
# to allow packets to flow: echo 1 > /proc/sys/net/ipv4/ip_forward
# iptables for your own machine: iptables -I INPUT -j NFQUEUE —queue-num 0
# iptables -I OUTPUT -j NFQUEUE —queue-num 0
# iptables for remote machine: iptables -I FORWARD -j NFQUEUE —queue-num 0
# to enable my own html: service apache2 start
