import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    message = "Hello World"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)
        client.sendto(message.encode("utf-8"), (HOST, PORT))
        print(f"[UDP CLIENT] Sent: {message!r}")

        data, _ = client.recvfrom(2048)
        reply = data.decode("utf-8", errors="replace")
        print(f"[UDP CLIENT] Received: {reply!r}")

if __name__ == "__main__":
    main()
