import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)

        pw = input("Nhập mật mã: ").strip()
        client.sendto(f"PASS:{pw}".encode("utf-8"), (HOST, PORT))

        try:
            data, _ = client.recvfrom(2048)
            resp = data.decode("utf-8", errors="replace")
        except socket.timeout:
            print("[CLIENT] Timeout (server không phản hồi).")
            return

        if not resp.startswith("OK"):
            print("[CLIENT]", resp)
            return

        print("[CLIENT] Xác thực thành công. Bắt đầu chat (nhấn 0 để thoát).")

        while True:
            msg = input("You: ").strip()
            client.sendto(msg.encode("utf-8"), (HOST, PORT))

            try:
                data, _ = client.recvfrom(4096)
                print("Server:", data.decode("utf-8", errors="replace"))
            except socket.timeout:
                print("Server: (timeout)")

            if msg == "0":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
