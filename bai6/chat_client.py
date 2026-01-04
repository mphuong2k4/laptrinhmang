import socket

def read_server_info():
    ip = input("Nhập IP server (mặc định 127.0.0.1): ").strip() or "127.0.0.1"
    p = input("Nhập PORT server (mặc định 5000): ").strip() or "5000"

    if not p.isdigit() or not (1 <= int(p) <= 65535):
        print("PORT không hợp lệ, dùng mặc định 5000.")
        p = "5000"

    return ip, int(p)

def main():
    server_ip, server_port = read_server_info()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)
        print(f"[UDP CLIENT] Chat tới {server_ip}:{server_port}")
        print("Nhập message để gửi. Nhấn 0 để thoát.")

        while True:
            msg = input("You: ").strip()
            client.sendto(msg.encode("utf-8"), (server_ip, server_port))

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
