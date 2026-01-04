import socket

def read_server_info():
    ip = input("Nhập IP server (mặc định 127.0.0.1): ").strip()
    if ip == "":
        ip = "127.0.0.1"

    s = input("Nhập PORT server (mặc định 5000): ").strip()
    if s == "":
        port = 5000
    elif s.isdigit() and 1 <= int(s) <= 65535:
        port = int(s)
    else:
        print("PORT không hợp lệ, dùng mặc định 5000.")
        port = 5000

    return ip, port

def main():
    server_ip, server_port = read_server_info()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_ip, server_port))
        print(f"[CLIENT] Connected to {server_ip}:{server_port}")
        print("Nhập message để gửi. Nhấn 0 để thoát.")

        while True:
            msg = input("You: ")

            client.sendall(msg.encode("utf-8"))

            data = client.recv(4096)
            if not data:
                print("[CLIENT] Server closed connection.")
                break

            reply = data.decode("utf-8", errors="replace")
            print(reply)

            if msg.strip() == "0":
                break

        print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
