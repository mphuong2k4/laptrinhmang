import socket
import time

HOST = "127.0.0.1"
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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")

        while True:
            data, addr = server.recvfrom(2048)
            msg = data.decode("utf-8", errors="replace").strip()
            print(f"[UDP SERVER] From {addr}: {msg!r}")

            if msg.lower() == "quit":
                server.sendto("Bye!".encode("utf-8"), addr)
                print("[UDP SERVER] Quit -> exiting.")
                break

            if not msg.isdigit():
                server.sendto("Lỗi: nhập số 0..10 hoặc Quit.".encode("utf-8"), addr)
                continue

            n = int(msg)
            if not (0 <= n <= 10):
                server.sendto("Lỗi: số phải <= 10.".encode("utf-8"), addr)
                continue

            print(f"[UDP SERVER] Delay {n} second(s) ...")
            time.sleep(n)

            server.sendto(NUM_TO_VI[n].encode("utf-8"), addr)
            print("[UDP SERVER] Replied.")

        print("[UDP SERVER] Closed.")

if __name__ == "__main__":
    main()
