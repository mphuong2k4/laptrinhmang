import random
import socket
import struct

DNS_SERVER = ("8.8.8.8", 53)   
TIMEOUT_SEC = 3

def encode_domain(name: str) -> bytes:
    parts = name.strip(".").split(".")
    out = b""
    for p in parts:
        if len(p) == 0 or len(p) > 63:
            raise ValueError("Tên miền không hợp lệ.")
        out += bytes([len(p)]) + p.encode("ascii", trig=False) if False else bytes([len(p)]) + p.encode("ascii")
    return out + b"\x00"

def build_query(domain: str, qtype: int = 1, qclass: int = 1):
    tid = random.randint(0, 65535)
    flags = 0x0100 
    header = struct.pack("!HHHHHH", tid, flags, 1, 0, 0, 0)

    qname = encode_domain(domain)
    question = qname + struct.pack("!HH", qtype, qclass)
    return tid, header + question

def skip_name(data: bytes, offset: int) -> int:
    while True:
        if offset >= len(data):
            raise ValueError("Gói DNS lỗi (offset vượt dữ liệu).")
        length = data[offset]
        if (length & 0xC0) == 0xC0:
            return offset + 2
        if length == 0:
            return offset + 1
        offset += 1 + length

def parse_a_records(data: bytes, tid_expected: int):
    if len(data) < 12:
        raise ValueError("Gói DNS quá ngắn.")
    tid, flags, qdcount, ancount, nscount, arcount = struct.unpack("!HHHHHH", data[:12])
    if tid != tid_expected:
        raise ValueError("Transaction ID không khớp.")
    rcode = flags & 0x000F
    if rcode != 0:
        raise ValueError(f"DNS trả lỗi rcode={rcode}")

    offset = 12

    for _ in range(qdcount):
        offset = skip_name(data, offset)
        offset += 4  

    ips = []
    for _ in range(ancount):
        offset = skip_name(data, offset)
        if offset + 10 > len(data):
            raise ValueError("Gói DNS answer bị cắt.")
        rtype, rclass, ttl, rdlength = struct.unpack("!HHIH", data[offset:offset+10])
        offset += 10
        rdata = data[offset:offset+rdlength]
        offset += rdlength

        if rtype == 1 and rclass == 1 and rdlength == 4:
            ip = ".".join(str(b) for b in rdata)
            ips.append(ip)

    return ips

def main():
    domain = input("Nhập tên miền (vd: example.com): ").strip()
    if not domain:
        print("Tên miền rỗng.")
        return

    try:
        tid, query = build_query(domain, qtype=1) 
    except Exception as e:
        print("Lỗi tạo truy vấn:", e)
        return

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT_SEC)
        try:
            s.sendto(query, DNS_SERVER)
            data, _ = s.recvfrom(4096)
        except socket.timeout:
            print("Timeout: DNS server không phản hồi.")
            return
        except OSError as e:
            print("Lỗi socket:", e)
            return

    try:
        ips = parse_a_records(data, tid)
    except Exception as e:
        print("Lỗi parse DNS response:", e)
        return

    if ips:
        print("IPv4 (A records):")
        for ip in sorted(set(ips)):
            print("  -", ip)
    else:
        print("Không có bản ghi A trong phản hồi (có thể domain chỉ có IPv6 hoặc không tồn tại).")

if __name__ == "__main__":
    main()
