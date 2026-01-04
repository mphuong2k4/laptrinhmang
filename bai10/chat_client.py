import socket

HOST = "127.0.0.1"
PORT = 5000

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(5)
            print(f"[UDP CLIENT] Ready to chat with {HOST}:{PORT}")
            print("Nhập message để gửi. Nhấn 0 để thoát. (Ctrl+C để dừng client)")

            while True:
                try:
                    msg = input("You: ").strip()
                except KeyboardInterrupt:
                    print("\n[UDP CLIENT] Dừng bởi Ctrl+C.")
                    break

                if msg == "":
                    print("[UDP CLIENT] Không được để help trống.")
                    continue

                try:
                    client.sendto(msg.encode("utf-8"), (HOST, PORT))
                except OSError as e:
                    print(f"[UDP CLIENT] Lỗi sendto(): {e}")
                    continue

                try:
                    data, _ = client.recvfrom(4096)
                    print("Server:", data.decode("utf-8", errors="replace"))
                except socket.timeout:
                    print("[UDP CLIENT] Timeout: server không phản hồi.")
                except OSError as e:
                    print(f"[UDP CLIENT] Lỗi recvfrom(): {e}")

                if msg == "0":
                    break

    except Exception as e:
        print(f"[UDP CLIENT] Lỗi không mong muốn: {e}")

    print("[UDP CLIENT] Closed.")

if __name__ == "__main__":
    main()
