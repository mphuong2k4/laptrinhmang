import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(10) 

            try:
                client.connect((HOST, PORT))
            except ConnectionRefusedError:
                print("[CLIENT] Không kết nối được: Server chưa chạy hoặc port sai.")
                return
            except socket.timeout:
                print("[CLIENT] Kết nối bị timeout.")
                return
            except OSError as e:
                print(f"[CLIENT] Lỗi connect(): {e}")
                return

            print(f"[CLIENT] Connected to {HOST}:{PORT}")
            print("Nhập message để gửi. Nhấn 0 để thoát. (Ctrl+C để dừng client)")

            while True:
                try:
                    msg = input("You: ")
                except KeyboardInterrupt:
                    print("\n[CLIENT] Dừng bởi Ctrl+C.")
                    break

                try:
                    client.sendall(msg.encode("utf-8"))
                except BrokenPipeError:
                    print("[CLIENT] Không gửi được: Server đã đóng kết nối.")
                    break
                except ConnectionResetError:
                    print("[CLIENT] Server đóng kết nối đột ngột (reset).")
                    break
                except socket.timeout:
                    print("[CLIENT] Gửi bị timeout.")
                    break
                except OSError as e:
                    print(f"[CLIENT] Lỗi send(): {e}")
                    break

                try:
                    data = client.recv(4096)
                except ConnectionResetError:
                    print("[CLIENT] Server reset khi đang nhận.")
                    break
                except socket.timeout:
                    print("[CLIENT] Nhận bị timeout.")
                    break
                except OSError as e:
                    print(f"[CLIENT] Lỗi recv(): {e}")
                    break

                if not data:
                    print("[CLIENT] Server đã đóng kết nối.")
                    break

                print("Server:", data.decode("utf-8", errors="replace"))

                if msg.strip() == "0":
                    break

    except Exception as e:
        print(f"[CLIENT] Lỗi không mong muốn: {e}")

    print("[CLIENT] Closed.")

if __name__ == "__main__":
    main()
