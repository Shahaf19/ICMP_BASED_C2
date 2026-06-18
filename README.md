# ICMP-Based Command and Control (C2)

A simple covert Command and Control (C2) framework that uses ICMP (ping) packets to communicate between a server controller and a client agent. The communication relies on embedding shell commands and their results directly in the raw data payloads of ICMP Echo Requests and Echo Replies.

## Files

- **`icmp_server.py`**: The controller script that listens for ICMP packets from an agent, prompts the operator to input shell commands, sends them to the agent, and logs the returned output to a file (`filename.txt`).
- **`icmp_client.py`**: The beaconing agent that periodically pings the server, listens for incoming commands, executes them on the local system, and returns the output in chunks via ICMP Echo Reply packets.

## Features

- **Covert Communication**: Embeds instructions within standard ICMP packet payloads, bypassing some traditional TCP/UDP monitoring.
- **Kernel-Level Tweaks (Server)**: Temporarily disables the OS kernel's default ICMP echo responses (`/proc/sys/net/ipv4/icmp_echo_ignore_all`) on the server to avoid noisy duplicate replies.
- **Chunked Data Transmission**: The client automatically chunks large command outputs into 500-byte segments to send back over ICMP.

## Prerequisites

- **Python 3.x**
- **Scapy** library (`pip install scapy`)
- **Root/Administrator Privileges**: Both scripts require raw socket access, meaning they must be run with elevated privileges (e.g., `sudo`).

## Configuration & Usage

### 1. Server setup
Before running [icmp_server.py](icmp_server.py), update the `interfaces` list at the bottom of the script to match your system's listening network interfaces (e.g., `['eth0']` or `['wlan0']`).

Start the server (Linux environment is utilized for the `/proc/sys` adjustments):
```bash
sudo python3 icmp_server.py
```

### 2. Client setup
Before running [icmp_client.py](icmp_client.py), update the `server_ip` variable to point to your server's IP address.

Start the client agent:
```bash
sudo python3 icmp_client.py
```

### 3. Execution
- The client emits ICMP Type 8 (Echo Request) packets to beacon the server.
- The server captures these beacons and prompts you to enter a command.
- Enter your shell command. It executes on the client system and the output is echoed back to the server and appended to `filename.txt`.

## Disclaimer

This project is intended for **educational and authorized testing purposes only**. Do not use this tool on networks or systems you do not own or have explicit authorization to assess.
