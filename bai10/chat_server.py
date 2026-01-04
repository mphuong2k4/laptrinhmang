import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                server.bind((HOST, PORT))
            except OSError as e:
                print(f"[SERVER] Không bind được {HOST}:{PORT}. Có thể port đang bận. ({e})")
                return

            server.listen(1)
            print(f"[SERVER] Listening on {HOST}:{PORT} ... (Ctrl+C để dừng)")

            while True:
                try:
                    conn, addr = server.accept()
                except KeyboardInterrupt:
                    print("\n[SERVER] Dừng bởi Ctrl+C.")
                    break
                except OSError as e:
                    print(f"[SERVER] Lỗi accept(): {e}")
                    break

                with conn:
                    print(f"[SERVER] Connected by {addr}")

                    while True:
                        try:
                            data = conn.recv(4096)
                        except ConnectionResetError:
                            print("[SERVER] Client đóng kết nối đột ngột (reset).")
                            break
                        except OSError as e:
                            print(f"[SERVER] Lỗi recv(): {e}")
                            break

                        if not data:
                            print("[SERVER] Client đã ngắt kết nối.")
                            break

                        msg = data.decode("utf-8", errors="replace").strip()
                        print(f"[SERVER] Received: {msg!r}")

                        try:
                            if msg == "0":
                                conn.sendall("Server: Bye!".encode("utf-8"))
                                print("[SERVER] Received 0 -> đóng kết nối client.")
                                break

                            reply = f"Đã nhận: {msg}"
                            conn.sendall(reply.encode("utf-8"))

                        except BrokenPipeError:
                            print("[SERVER] Không gửi được (Broken pipe) - client đã đóng.")
                            break
                        except ConnectionResetError:
                            print("[SERVER] Client reset khi đang gửi.")
                            break
                        except OSError as e:
                            print(f"[SERVER] Lỗi send(): {e}")
                            break

                print("[SERVER] Chờ client mới...")

    except Exception as e:
        print(f"[SERVER] Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
