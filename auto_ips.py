import subprocess
import time
import os

LOG_PATH = "/opt/zeek/logs/current/conn.log"
PFSENSE_IP = "192.168.209.138"
PFSENSE_USER = "root"
BYTE_THRESHOLD = 5000000

def block_ip(ip_address):
    print(f"[ACTION] AI executing mitigation rule for IP: {ip_address}")
    try:
        cmd = f"ssh -o StrictHostKeyChecking=no {PFSENSE_USER}@{PFSENSE_IP} 'pfctl -t zeek_block -T add {ip_address}'"
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[SUCCESS] Target {ip_address} has been permanently isolated.")
    except subprocess.CalledProcessError:
        print(f"[FAILED] Could not execute isolation rule for {ip_address}")

def analyze_stream(line):
    cols = line.strip().split('\t')
    if len(cols) > 9:
        src_ip = cols[2]

        try:
            orig_bytes = int(cols[9]) if cols[9] != '-' else 0
        except (ValueError, IndexError):
            return

        risk_score = 48.00
        if orig_bytes > BYTE_THRESHOLD:
            risk_score = 100.00

        print(f"[*] Analyzing IP {src_ip} | Bytes sent: {orig_bytes} | Risk Score: {risk_score:.2f}%")

        if risk_score == 100.00:
            print(f"[ALERT] Malicious flow from {src_ip} | Risk Score: {risk_score:.2f}%")
            block_ip(src_ip)

def main():
    print("[*] Initializing AI-Driven IPS (Safe Mode)...")

    if not os.path.exists(LOG_PATH):
        open(LOG_PATH, 'a').close()

    with open(LOG_PATH, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.5)
                continue

            if not line.startswith('#'):
                analyze_stream(line)

if __name__ == "__main__":
    main()
