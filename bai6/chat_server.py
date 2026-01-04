import socket

def read_bind_info():
    host = input("Nhập IP bind server (mặc định 0.0.0.0): ").strip() or "0.0.0.0"
    p = input("Nhập PORT server (mặc định 5000): ").strip() or "5000"

    if not p.isdigit() or not (1 <= int(p) <= 65535):
        print("PORT không hợp lệ, dùng mặc định 5000.")
        p = "5000"

    return host, int(p)

def main():
    host, port = read_bind_info()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        try:
            server.bind((host, port))
        except OSError as e:
            print(f"[UDP SERVER] Không bind được {host}:{port}. ({e})")
            return

        print(f"[UDP SERVER] Listening on {host}:{port} ...")

        while True:
            data, addr = server.recvfrom(4096)
            msg = data.decode("utf-8", errors="replace").strip()
            print(f"[UDP SERVER] From {addr}: {msg!r}")

            if msg == "0":
                server.sendto("Server: Bye!".encode("utf-8"), addr)
                print("[UDP SERVER] Received 0 -> exiting.")
                break

            reply = f"Đã nhận: {msg}"
            server.sendto(reply.encode("utf-8"), addr)

        print("[UDP SERVER] Closed.")

if __name__ == "__main__":
    main()
