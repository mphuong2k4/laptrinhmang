import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)  
        print(f"[UDP CLIENT] Ready to chat with {HOST}:{PORT}")
        print("Nhập message để gửi. Nhấn 0 để thoát.")

        while True:
            msg = input("You: ").strip()
            client.sendto(msg.encode("utf-8"), (HOST, PORT))

            try:
                data, _ = client.recvfrom(4096)
                print("Server:", data.decode("utf-8", errors="replace"))
            except socket.timeout:
                print("Server: (timeout - không nhận được phản hồi)")

            if msg == "0":
                break

        print("[UDP CLIENT] Closed.")

if __name__ == "__main__":
    main()
