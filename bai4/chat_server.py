import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")

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
