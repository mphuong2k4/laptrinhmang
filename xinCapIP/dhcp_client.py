import random
from scapy.all import (
    Ether, IP, UDP, BOOTP, DHCP,
    conf, get_if_hwaddr, sendp, sniff
)

DNS_TIMEOUT = 8

def mac_to_chaddr(mac: str) -> bytes:
    # BOOTP chaddr field: 16 bytes (MAC 6 bytes + padding)
    return bytes.fromhex(mac.replace(":", "")) + b"\x00" * 10

def get_option_value(dhcp_options, key: str):
    """
    Scapy DHCP options can contain:
      - ('key', value)
      - ('key', v1, v2, ...)
      - 'end'
    So we safely parse:
      - key = opt[0]
      - value = opt[1] (ignore extra)
    """
    for opt in dhcp_options:
        if isinstance(opt, tuple) and len(opt) >= 2:
            k = opt[0]
            v = opt[1]
            if k == key:
                return v
    return None

def dhcp_discover(iface: str, timeout: int = 8):
    mac = get_if_hwaddr(iface)
    xid = random.randint(1, 0xFFFFFFFF)

    pkt = (
        Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=mac_to_chaddr(mac), xid=xid, flags=0x8000) /
        DHCP(options=[
            ("message-type", "discover"),
            ("param_req_list", [1, 3, 6, 15, 51, 54, 58, 59]),  # subnet, router, dns, domain, lease, server_id, T1, T2
            "end"
        ])
    )

    print(f"[+] Sending DHCPDISCOVER on iface={iface}, mac={mac}, xid={xid}")
    sendp(pkt, iface=iface, verbose=False)

    def is_offer(p):
        if not (p.haslayer(DHCP) and p.haslayer(BOOTP)):
            return False
        if p[BOOTP].xid != xid:
            return False
        # message-type = 2 (offer)
        for opt in p[DHCP].options:
            if isinstance(opt, tuple) and len(opt) >= 2 and opt[0] == "message-type" and opt[1] == 2:
                return True
        return False

    offers = sniff(iface=iface, lfilter=is_offer, timeout=timeout)
    return xid, mac, offers

def dhcp_request(iface: str, xid: int, mac: str, offer_pkt, timeout: int = 8):
    yiaddr = offer_pkt[BOOTP].yiaddr  # offered IP
    server_id = get_option_value(offer_pkt[DHCP].options, "server_id")
    subnet = get_option_value(offer_pkt[DHCP].options, "subnet_mask")
    router = get_option_value(offer_pkt[DHCP].options, "router")
    dns = get_option_value(offer_pkt[DHCP].options, "name_server")
    lease = get_option_value(offer_pkt[DHCP].options, "lease_time")

    if not server_id:
        # Một số DHCP server/relay có thể thiếu server_id trong offer (hiếm), nhưng thường có
        raise RuntimeError("Không tìm thấy server_id trong DHCPOFFER.")

    pkt = (
        Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) /
        IP(src="0.0.0.0", dst="255.255.255.255") /
        UDP(sport=68, dport=67) /
        BOOTP(chaddr=mac_to_chaddr(mac), xid=xid, flags=0x8000) /
        DHCP(options=[
            ("message-type", "request"),
            ("requested_addr", yiaddr),
            ("server_id", server_id),
            ("param_req_list", [1, 3, 6, 15, 51, 54, 58, 59]),
            "end"
        ])
    )

    print(f"[+] Got DHCPOFFER: offered_ip={yiaddr}, server_id={server_id}")
    print("[+] Sending DHCPREQUEST...")
    sendp(pkt, iface=iface, verbose=False)

    def is_ack(p):
        if not (p.haslayer(DHCP) and p.haslayer(BOOTP)):
            return False
        if p[BOOTP].xid != xid:
            return False
        # message-type = 5 (ack)
        for opt in p[DHCP].options:
            if isinstance(opt, tuple) and len(opt) >= 2 and opt[0] == "message-type" and opt[1] == 5:
                return True
        return False

    acks = sniff(iface=iface, lfilter=is_ack, timeout=timeout)
    return yiaddr, server_id, subnet, router, dns, lease, acks

def main():
    print("Các interface khả dụng:")
    ifaces = list(conf.ifaces.values())
    for i, itf in enumerate(ifaces):
        desc = getattr(itf, "description", itf.name)
        print(f"  [{i}] {desc}")

    idx = input("Chọn số interface để xin DHCP (vd 0): ").strip()
    if not idx.isdigit():
        print("Index không hợp lệ.")
        return

    idx = int(idx)
    if idx < 0 or idx >= len(ifaces):
        print("Index ngoài phạm vi.")
        return

    iface = ifaces[idx].name

    xid, mac, offers = dhcp_discover(iface, timeout=DNS_TIMEOUT)
    if len(offers) == 0:
        print("[-] Không nhận được DHCPOFFER (thiếu Npcap? chưa chạy Admin? mạng chặn broadcast?).")
        return

    offer = offers[0]

    try:
        yiaddr, server_id, subnet, router, dns, lease, acks = dhcp_request(iface, xid, mac, offer, timeout=DNS_TIMEOUT)
    except Exception as e:
        print("[-] Lỗi khi gửi DHCPREQUEST:", e)
        return

    if len(acks) == 0:
        print("[-] Không nhận được DHCPACK.")
        return

    # ACK có thể chứa options đầy đủ hơn OFFER
    ack = acks[0]
    subnet_ack = get_option_value(ack[DHCP].options, "subnet_mask") or subnet
    router_ack = get_option_value(ack[DHCP].options, "router") or router
    dns_ack = get_option_value(ack[DHCP].options, "name_server") or dns
    lease_ack = get_option_value(ack[DHCP].options, "lease_time") or lease
    server_id_ack = get_option_value(ack[DHCP].options, "server_id") or server_id

    print("\n✅ DHCPACK nhận được!")
    print(f"IP được cấp: {yiaddr}")
    print(f"DHCP Server: {server_id_ack}")
    if subnet_ack:
        print(f"Subnet mask: {subnet_ack}")
    if router_ack:
        print(f"Gateway/Router: {router_ack}")
    if dns_ack:
        print(f"DNS: {dns_ack}")
    if lease_ack:
        print(f"Lease time (s): {lease_ack}")

    print("\nLưu ý: Script demo xin IP và in thông tin, KHÔNG tự cấu hình IP cho Windows.")

if __name__ == "__main__":
    main()
