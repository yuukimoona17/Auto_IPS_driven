# AI-Driven Automated Response IPS

## Project Overview
Modern Intrusion Detection Systems (IDS) often operate in a passive mode, meaning they only generate alerts when anomalous traffic is detected, leaving the network vulnerable until a human administrator manually intervenes. 

Inspired by the pain points discussed in recent cybersecurity research (AI-Driven Dynamic Firewall Optimization, arXiv: 2506.05356), this project implements an Active Automated Response IPS. It bridges the gap between AI detection and network mitigation by creating a closed-loop defense mechanism: Detect (Zeek) -> Analyze (Python AI Engine) -> Mitigate (pfSense).

## System Architecture
The lab environment is built on VMware simulating an enterprise network:
*   Target Server (Ubuntu 64-bit): Acts as the victim machine. Runs Zeek IDS to monitor incoming traffic and the Python AI Engine to analyze logs.
*   Firewall (FreeBSD / pfSense): The core router. Configured with a blocklist table (zeek_block).
*   Attacker Client (Ubuntu Desktop): Simulates a threat actor injecting massive malicious payloads.

### Workflow
1.  Traffic Generation: The attacker sends a high-volume data stream (>5MB) to the target server.
2.  Flow Analysis: Zeek IDS captures the traffic (bypassing checksum offloading) and writes flow features to conn.log.
3.  Real-time AI Scoring: auto_ips.py continuously tails the log file, parses the parameters, and assigns a dynamic Risk Score.
4.  Automated Mitigation: If the Risk Score hits 100%, the engine automatically connects to the pfSense firewall via SSH (bypassing strict host key checks) and pushes a pfctl command to permanently isolate the attacker's IP.

## Repository Structure
.
├── auto_ips.py          # The core AI engine and mitigation script (Server)
├── attack.py            # The simulated payload generator (Client)
├── README.md            # Project documentation
└── images/              # Proof of Concept screenshots
    ├── alert_success.jpg 
    └── pfsense_block.jpg

## Prerequisites

* Zeek IDS installed on the Ubuntu Server (/opt/zeek/).
* pfSense with SSH enabled and a firewall alias/table named zeek_block initialized.
* SSH Keys / Passwords configured for the script to access pfSense as root.

## How to Run the Simulation

### 1. Prepare the Target Server (Ubuntu)

Disable network checksum offloading to ensure Zeek captures internal VM traffic properly:

sudo ethtool -K ens33 rx off tx off


Open a port to receive the raw payload:
while true; do nc -l 9999 > /dev/null; done

Start the AI-Driven IPS Engine:
sudo python3 auto_ips.py


### 2. Prepare the Firewall (pfSense)

(Optional) Flush previous block states before testing:
pfctl -F states
pfctl -t zeek_block -T flush

### 3. Launch the Attack (Client)

Run the attack script to deliver a 6MB payload to the target server:
python3 attack.py``

## Expected Results

* On the Client: The script will successfully send the payload, but subsequent connection attempts will face a Connection timed out or Broken pipe as the IP gets blocked.
* On the Server: The IPS engine will output:
[*] Analyzing IP 192.168.209.148 | Bytes sent: 6291456 | Risk Score: 100.00%
[ALERT] Malicious flow from 192.168.209.148 | Risk Score: 100.00%
[ACTION] AI executing mitigation rule for IP: 192.168.209.148
[SUCCESS] Target 192.168.209.148 has been permanently isolated.



