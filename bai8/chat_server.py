import socket

HOST = "127.0.0.1"
PORT = 5000

PASSWORD = "123456"  

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")

        conn, addr = server.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")

            data = conn.recv(1024)
            if not data:
                print("[SERVER] No auth data -> close.")
                return

            client_pass = data.decode("utf-8", errors="replace").strip()
            if client_pass != PASSWORD:
                conn.sendall("ERROR: Sai mật mã!".encode("utf-8"))
                print("[SERVER] Wrong password -> closed.")
                return

            conn.sendall("OK".encode("utf-8"))
            print("[SERVER] Auth OK. Start chatting...")

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
