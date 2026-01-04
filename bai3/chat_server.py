import socket

HOST = "0.0.0.0"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")

        conn, addr = server.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")

            data = conn.recv(4096)
            msg = data.decode("utf-8", errors="replace").strip()
            print(f"[SERVER] Received: {msg}")

            reply = f"Đã nhận: {msg}"
            conn.sendall(reply.encode("utf-8"))
            print("[SERVER] Replied and exiting.")

if __name__ == "__main__":
    main()
