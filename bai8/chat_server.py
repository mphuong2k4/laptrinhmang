import socket

HOST = "127.0.0.1"
PORT = 5000
PASSWORD = "123456" 

authed_clients = set()  

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")

        while True:
            data, addr = server.recvfrom(4096)
            msg = data.decode("utf-8", errors="replace").strip()
            print(f"[UDP SERVER] From {addr}: {msg!r}")

            if addr not in authed_clients:
                if msg.startswith("PASS:"):
                    pw = msg[5:]
                    if pw == PASSWORD:
                        authed_clients.add(addr)
                        server.sendto("OK".encode("utf-8"), addr)
                        print(f"[UDP SERVER] Auth OK for {addr}")
                    else:
                        server.sendto("ERROR: Sai mật mã!".encode("utf-8"), addr)
                        print(f"[UDP SERVER] Auth FAIL for {addr}")
                else:
                    server.sendto("ERROR: Chưa xác thực. Gửi PASS:<matkhau>".encode("utf-8"), addr)
                continue

            if msg == "0":
                server.sendto("Server: Bye!".encode("utf-8"), addr)
                authed_clients.discard(addr)
                print(f"[UDP SERVER] {addr} exit -> removed auth.")
                continue

            reply = f"Đã nhận: {msg}"
            server.sendto(reply.encode("utf-8"), addr)

if __name__ == "__main__":
    main()
