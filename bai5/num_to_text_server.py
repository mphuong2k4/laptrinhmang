import socket

HOST = "0.0.0.0"
PORT = 5000

NUM_TO_VI = {
    0: "không",
    1: "một",
    2: "hai",
    3: "ba",
    4: "bốn",
    5: "năm",
    6: "sáu",
    7: "bảy",
    8: "tám",
    9: "chín",
    10: "mười",
}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[SERVER] Listening on {HOST}:{PORT} ...")

        conn, addr = server.accept()
        with conn:
            print(f"[SERVER] Connected by {addr}")

            while True:
                data = conn.recv(1024)
                if not data:
                    print("[SERVER] Client disconnected.")
                    break

                msg = data.decode("utf-8", errors="replace").strip()
                print(f"[SERVER] Received: {msg!r}")

                if msg.lower() == "quit":
                    conn.sendall("Bye!".encode("utf-8"))
                    print("[SERVER] Quit -> exiting.")
                    break

                if not msg.isdigit():
                    conn.sendall("Lỗi: hãy nhập số tự nhiên từ 0 đến 10 hoặc Quit.".encode("utf-8"))
                    continue

                n = int(msg)
                if 0 <= n <= 10:
                    conn.sendall(NUM_TO_VI[n].encode("utf-8"))
                else:
                    conn.sendall("Lỗi: số phải <= 10.".encode("utf-8"))

        print("[SERVER] Closed.")

if __name__ == "__main__":
    main()
