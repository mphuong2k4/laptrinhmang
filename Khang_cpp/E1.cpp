#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>

#pragma comment(lib, "ws2_32.lib")

void apply_tcp_optimization(SOCKET s) {
    // 1. Vô hiệu hóa thuật toán Nagle (TCP_NODELAY)
    // Giúp gửi dữ liệu ngay lập tức thay vì đợi gom đủ gói tin lớn.
    BOOL nodelay = TRUE;
    if (setsockopt(s, IPPROTO_TCP, TCP_NODELAY, (char*)&nodelay, sizeof(nodelay)) == 0) {
        std::cout << "[OK] TCP_NODELAY enabled (Reduced Latency)\n";
    }

    // 2. Tăng kích thước bộ đệm (Buffer Tuning)
    // Tăng lên 1MB để tối ưu cho việc truyền tải dữ liệu lớn.
    int buffer_size = 1024 * 1024;
    setsockopt(s, SOL_SOCKET, SO_SNDBUF, (char*)&buffer_size, sizeof(buffer_size));
    setsockopt(s, SOL_SOCKET, SO_RCVBUF, (char*)&buffer_size, sizeof(buffer_size));
    std::cout << "[OK] Buffer sizes set to 1MB (Higher Throughput)\n";

    // 3. Kích hoạt KeepAlive
    // Tự động kiểm tra nếu kết nối còn sống hay không sau một khoảng thời gian.
    BOOL keepalive = TRUE;
    if (setsockopt(s, SOL_SOCKET, SO_KEEPALIVE, (char*)&keepalive, sizeof(keepalive)) == 0) {
        std::cout << "[OK] SO_KEEPALIVE enabled\n";
    }

    // 4. Cấu hình Reuse Address (Hữu ích khi Server khởi động lại nhanh)
    BOOL reuse = TRUE;
    setsockopt(s, SOL_SOCKET, SO_REUSEADDR, (char*)&reuse, sizeof(reuse));
}

int main() {
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);

    SOCKET server_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server_sock != INVALID_SOCKET) {
        apply_tcp_optimization(server_sock);
    }

    // ... Tiếp tục các bước bind, listen như bình thường ...

    closesocket(server_sock);
    WSACleanup();
    return 0;
}
