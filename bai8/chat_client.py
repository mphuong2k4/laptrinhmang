import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(f"[CLIENT] Connected to {HOST}:{PORT}")

        password = input("Nhập mật mã: ").strip()
        client.sendall(password.encode("utf-8"))

        data = client.recv(1024)
        if not data:
            print("[CLIENT] Server closed during auth.")
            return

        resp = data.decode("utf-8", errors="replace")
        if not resp.startswith("OK"):
            print("[CLIENT]", resp)
            return

        print("[CLIENT] Xác thực thành công. Bắt đầu chat (nhấn 0 để thoát).")

        while True:
            msg = input("You: ")
            client.sendall(msg.encode("utf-8"))

            data = client.recv(4096)
            if not data:
                print("[CLIENT] Server closed connection.")
                break

            print("Server:", data.decode("utf-8", errors="replace"))

            if msg.strip() == "0":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
