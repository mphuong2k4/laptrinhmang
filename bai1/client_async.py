import asyncio

HOST = "127.0.0.1"
PORT = 9000

async def receiver(reader: asyncio.StreamReader):
    """Luồng nhận phản hồi từ server (in ra ngay khi có)."""
    while True:
        line = await reader.readline()
        if not line:
            print("\n[!] Server closed connection.")
            return
        print(f"\n<<< Server reply: {line.decode().strip()}")
        print(">>> Enter seconds (or 'q' to quit): ", end="", flush=True)

async def sender(writer: asyncio.StreamWriter):
    """
    Luồng nhập từ bàn phím KHÔNG block event loop:
    dùng asyncio.to_thread để chạy input() trên thread phụ.
    """
    while True:
        s = await asyncio.to_thread(input, ">>> Enter seconds (or 'q' to quit): ")
        s = s.strip()

        if s.lower() in ("q", "quit", "exit"):
            writer.close()
            await writer.wait_closed()
            return

        if not s:
            continue

        try:
            int(s)
        except ValueError:
            print("Please enter an integer (e.g., 2, 10).")
            continue

        writer.write((s + "\n").encode())
        await writer.drain()

async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("Connected to server.")

    await asyncio.gather(
        receiver(reader),
        sender(writer),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
