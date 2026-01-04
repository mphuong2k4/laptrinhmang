import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)
        print(f"[UDP CLIENT] Ready to send to {HOST}:{PORT}")
        print("Nhập số (0..10) để gửi. Gõ Quit để thoát.")

        while True:
            msg = input("Input: ").strip()
            if msg == "":
                continue

            client.sendto(msg.encode("utf-8"), (HOST, PORT))

            try:
                data, _ = client.recvfrom(2048)
                reply = data.decode("utf-8", errors="replace")
                print("Server reply:", reply)
            except socket.timeout:
                print("Server reply: (timeout)")
                continue

            if msg.lower() == "quit":
                break

        print("[UDP CLIENT] Closed.")

if __name__ == "__main__":
    main()
