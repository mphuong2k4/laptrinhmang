import socket

HOST = "0.0.0.0"
PORT = 5000
SHIFT = 1  

def caesar_shift(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            base = ord("A")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        elif "a" <= ch <= "z":
            base = ord("a")
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)

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
                data = conn.recv(4096)
                if not data:
                    print("[SERVER] Client disconnected.")
                    break

                cipher = data.decode("utf-8", errors="replace").strip()

                if cipher == "0":
                    bye_cipher = caesar_shift("Server: Bye!", SHIFT)  
                    conn.sendall(bye_cipher.encode("utf-8"))
                    print("[SERVER] Received 0 -> exiting.")
                    break

                plain = caesar_shift(cipher, -SHIFT) 
                print(f"[SERVER] Cipher received: {cipher!r}")
                print(f"[SERVER] Plain decoded : {plain!r}")

                reply_plain = f"Đã nhận: {plain}"
                reply_cipher = caesar_shift(reply_plain, SHIFT)  
                conn.sendall(reply_cipher.encode("utf-8"))

        print("[SERVER] Closed.")

if __name__ == "__main__":
    main()
