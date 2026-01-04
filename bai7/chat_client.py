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
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(5)
        print(f"[UDP CLIENT] Chat tới {HOST}:{PORT}")
        print("Nhập message (plaintext). Nhấn 0 để thoát.")

        while True:
            plain = input("You: ")

            if plain.strip() == "0":
                client.sendto(b"0", (HOST, PORT))
                try:
                    data, _ = client.recvfrom(4096)
                    bye_plain = caesar_shift(data.decode("utf-8", errors="replace"), -SHIFT)
                    print("Server:", bye_plain)
                except socket.timeout:
                    print("Server: (timeout)")
                break

            cipher = caesar_shift(plain, SHIFT)
            print(f"[UDP CLIENT] Cipher sent: {cipher!r}")
            client.sendto(cipher.encode("utf-8"), (HOST, PORT))

            try:
                data, _ = client.recvfrom(4096)
                reply_cipher = data.decode("utf-8", errors="replace")
                reply_plain = caesar_shift(reply_cipher, -SHIFT)
                print("Server:", reply_plain)
            except socket.timeout:
                print("Server: (timeout - không nhận được phản hồi)")

        print("[UDP CLIENT] Closed.")

if __name__ == "__main__":
    main()
