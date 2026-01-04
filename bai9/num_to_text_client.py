import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(f"[CLIENT] Connected to {HOST}:{PORT}")
        print("Nhập số (0..10) để gửi. Gõ Quit để thoát.")

        while True:
            msg = input("Input: ").strip()
            if msg == "":
                continue

            client.sendall(msg.encode("utf-8"))

            data = client.recv(1024)
            if not data:
                print("[CLIENT] Server closed connection.")
                break

            print("Server reply:", data.decode("utf-8", errors="replace"))

            if msg.lower() == "quit":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
