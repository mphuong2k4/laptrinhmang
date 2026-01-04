import socket

SERVER_IP = "127.0.0.1"   
SERVER_PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}")
        print("Nhập số tự nhiên (0..10) để gửi lên server. Gõ Quit để thoát.")

        while True:
            msg = input("Input: ").strip()
            if msg == "":
                continue

            client.sendall(msg.encode("utf-8"))

            data = client.recv(1024)
            if not data:
                print("[CLIENT] Server closed connection.")
                break

            reply = data.decode("utf-8", errors="replace")
            print("Server reply:", reply)

            if msg.lower() == "quit":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
