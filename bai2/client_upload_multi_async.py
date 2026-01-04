import asyncio
import os
import sys
import time

HOST = "127.0.0.1"
PORT = 9001
CHUNK = 64 * 1024  

async def upload_one_file(path: str, host: str, port: int):
    if not os.path.isfile(path):
        print(f"[!] Not found: {path}")
        return

    size = os.path.getsize(path)
    name = os.path.basename(path)

    reader, writer = await asyncio.open_connection(host, port)

    writer.write(f"{name}|{size}\n".encode())
    await writer.drain()

    resp = await reader.readline()
    if not resp:
        print(f"[{name}] Server no response.")
        writer.close()
        await writer.wait_closed()
        return

    resp = resp.decode(errors="ignore").strip()
    if not resp.startswith("OK|"):
        print(f"[{name}] Server error: {resp}")
        writer.close()
        await writer.wait_closed()
        return

    saved_name = resp.split("|", 1)[1]
    print(f"[{name}] -> server will save as: {saved_name}")

    sent = 0
    start = time.time()
    last_print = 0

    f = open(path, "rb")
    try:
        while sent < size:
            data = await asyncio.to_thread(f.read, CHUNK)
            if not data:
                break

            writer.write(data)
            await writer.drain()
            sent += len(data)

            pct = int(sent * 100 / size) if size > 0 else 100
            if pct - last_print >= 5 or pct == 100:
                elapsed = max(1e-6, time.time() - start)
                speed = sent / elapsed / (1024 * 1024)  
                print(f"[{name}] {pct}%  ({sent}/{size} bytes)  {speed:.2f} MB/s")
                last_print = pct

        done = await reader.readline()
        if done:
            print(f"[{name}] Server: {done.decode().strip()}")

    finally:
        f.close()
        writer.close()
        await writer.wait_closed()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client_upload_multi_async.py file1.mp3 file2.mp4 ...")
        return

    files = sys.argv[1:]
    tasks = [upload_one_file(p, HOST, PORT) for p in files]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
