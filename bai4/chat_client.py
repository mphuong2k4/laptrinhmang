import socket

SERVER_IP = "127.0.0.1"   
SERVER_PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}")
        print("Nhập message để gửi. Nhấn 0 để thoát.")

        while True:
            msg = input("You: ")

            client.sendall(msg.encode("utf-8"))

            data = client.recv(4096)
            if not data:
                print("[CLIENT] Server closed connection.")
                break

            reply = data.decode("utf-8", errors="replace")
            print("Server:", reply)

            if msg == "0":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
