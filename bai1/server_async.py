import asyncio

HOST = "127.0.0.1"
PORT = 9000

async def process_request(n: int, writer: asyncio.StreamWriter):
    await asyncio.sleep(n)
    writer.write(f"{n}\n".encode())   
    await writer.drain()

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"[+] Connected: {addr}")
    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            msg = line.decode().strip()
            if not msg:
                continue

            try:
                n = int(msg)
            except ValueError:
                writer.write(b"ERR\n")
                await writer.drain()
                continue

            asyncio.create_task(process_request(n, writer))

    finally:
        print(f"[-] Disconnected: {addr}")
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Server listening on {HOST}:{PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
