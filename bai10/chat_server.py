import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            try:
                server.bind((HOST, PORT))
            except OSError as e:
                print(f"[UDP SERVER] Không bind được {HOST}:{PORT}. Có thể port đang bận. ({e})")
                return

            print(f"[UDP SERVER] Listening on {HOST}:{PORT} ... (Ctrl+C để dừng)")

            while True:
                try:
                    data, addr = server.recvfrom(4096)
                except KeyboardInterrupt:
                    print("\n[UDP SERVER] Dừng bởi Ctrl+C.")
                    break
                except OSError as e:
                    print(f"[UDP SERVER] Lỗi recvfrom(): {e}")
                    break

                msg = data.decode("utf-8", errors="replace").strip()
                print(f"[UDP SERVER] From {addr}: {msg!r}")

                try:
                    if msg == "0":
                        server.sendto("Server: Bye!".encode("utf-8"), addr)
                        print("[UDP SERVER] Received 0 -> exiting.")
                        break

                    reply = f"Đã nhận: {msg}"
                    server.sendto(reply.encode("utf-8"), addr)

                except OSError as e:
                    print(f"[UDP SERVER] Lỗi sendto(): {e}")
                    continue

    except Exception as e:
        print(f"[UDP SERVER] Lỗi không mong muốn: {e}")

    print("[UDP SERVER] Closed.")

if __name__ == "__main__":
    main()
