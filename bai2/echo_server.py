import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")

        data, addr = server.recvfrom(2048)
        msg = data.decode("utf-8", errors="replace").strip()
        print(f"[UDP SERVER] Received from {addr}: {msg!r}")

        reply = f"Đã nhận {msg.upper()}"
        server.sendto(reply.encode("utf-8"), addr)
        print("[UDP SERVER] Replied and exiting.")

if __name__ == "__main__":
    main()
