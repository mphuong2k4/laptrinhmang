import socket

HOST = "127.0.0.1"
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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT} ...")

        while True:
            data, addr = server.recvfrom(4096)
            cipher = data.decode("utf-8", errors="replace").strip()

            if cipher == "0":
                bye_cipher = caesar_shift("Server: Bye!", SHIFT)  
                server.sendto(bye_cipher.encode("utf-8"), addr)
                print("[UDP SERVER] Received 0 -> exiting.")
                break

            plain = caesar_shift(cipher, -SHIFT) 
            print(f"[UDP SERVER] From {addr}")
            print(f"  Cipher received: {cipher!r}")
            print(f"  Plain decoded : {plain!r}")

            reply_plain = f"Đã nhận: {plain}"
            reply_cipher = caesar_shift(reply_plain, SHIFT)  
            server.sendto(reply_cipher.encode("utf-8"), addr)

        print("[UDP SERVER] Closed.")

if __name__ == "__main__":
    main()
