import asyncio
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9001
UPLOAD_DIR = "uploads"
CHUNK = 64 * 1024 

def make_saved_name(original_name: str) -> str:
    base = os.path.basename(original_name)
    _, ext = os.path.splitext(base)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{ts}{ext.lower()}"

async def handle_one_upload(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    try:
        header = await reader.readline()
        if not header:
            writer.close()
            await writer.wait_closed()
            return

        header = header.decode(errors="ignore").strip()
        parts = header.split("|", 1)
        if len(parts) != 2:
            writer.write(b"ERR bad header\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        original_name, size_str = parts[0], parts[1]
        try:
            total_size = int(size_str)
        except ValueError:
            writer.write(b"ERR bad size\n")
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            return

        saved_name = make_saved_name(original_name)
        save_path = os.path.join(UPLOAD_DIR, saved_name)

        writer.write(f"OK|{saved_name}\n".encode())
        await writer.drain()

        received = 0
        last_print = -1  

        print(f"[+] {addr} uploading '{original_name}' ({total_size} bytes) -> {save_path}")

        with open(save_path, "wb") as f:
            while received < total_size:
                to_read = min(CHUNK, total_size - received)
                chunk = await reader.readexactly(to_read)
                f.write(chunk)
                received += len(chunk)

                pct = int(received * 100 / total_size) if total_size > 0 else 100
                step = pct // 5
                if step != last_print:
                    last_print = step
                    print(f"    [server] {saved_name}: {pct}%")

        print(f"[✓] Saved: {save_path} ({received} bytes)")
        writer.write(b"DONE\n")
        await writer.drain()

    except asyncio.IncompleteReadError:
        print(f"[!] {addr} disconnected mid-upload.")
    except Exception as e:
        print(f"[!] Error from {addr}: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def main():
    server = await asyncio.start_server(handle_one_upload, HOST, PORT)
    print(f"Upload Server listening on {HOST}:{PORT} (save to ./{UPLOAD_DIR}/)")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
