import socket

SERVER_IP = "127.0.0.1"  
SERVER_PORT = 5000

def main():
    message = "Hello World"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}")

        client.sendall(message.encode("utf-8"))
        print(f"[CLIENT] Sent: {message!r}")

        data = client.recv(1024)
        reply = data.decode("utf-8", errors="replace")
        print(f"[CLIENT] Received: {reply!r}")

if __name__ == "__main__":
    main()
