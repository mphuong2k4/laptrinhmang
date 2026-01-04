import socket

HOST = "0.0.0.0"

def read_port():
    s = input("Nhập PORT server (mặc định 5000): ").strip()
    if s == "":
        return 5000
    if not s.isdigit():
        print("PORT không hợp lệ, dùng mặc định 5000.")
        return 5000
    port = int(s)
    if not (1 <= port <= 65535):
        print("PORT khác 1..65535, dùng mặc định 5000.")
        return 5000
    return port

def main():
    port = read_port()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        server.listen(1)
        print(f"[SERVER] Listening on {HOST}:{port} ...")

        conn, addr = server.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")

            while True:
                data = conn.recv(4096)
                if not data:
                    print("[SERVER] Client disconnected.")
                    break

                msg = data.decode("utf-8", errors="replace").strip()
                print(f"[SERVER] Received: {msg!r}")

                if msg == "0":
                    conn.sendall("Server: Bye!".encode("utf-8"))
                    print("[SERVER] Received 0 -> exiting.")
                    break

                reply = f"Đã nhận: {msg}"
                conn.sendall(reply.encode("utf-8"))

        print("[SERVER] Closed.")

if __name__ == "__main__":
    main()
