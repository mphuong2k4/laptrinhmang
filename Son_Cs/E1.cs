using System;
using System.Net;
using System.Net.Sockets;

class TcpOptimizationDemo
{
    static void ApplyTcpOptimization(Socket socket)
    {
        // 1. Disable Nagle Algorithm (TCP_NODELAY)
        socket.NoDelay = true;
        Console.WriteLine("[OK] TCP_NODELAY enabled (Reduced Latency)");

        // 2. Buffer Tuning (1MB)
        int bufferSize = 1024 * 1024;
        socket.SendBufferSize = bufferSize;
        socket.ReceiveBufferSize = bufferSize;
        Console.WriteLine("[OK] Buffer sizes set to 1MB (Higher Throughput)");

        // 3. Enable KeepAlive
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.KeepAlive, true);
        Console.WriteLine("[OK] SO_KEEPALIVE enabled");

        // 4. Enable Reuse Address
        socket.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        Console.WriteLine("[OK] SO_REUSEADDR enabled");
    }

    static void Main()
    {
        Socket serverSocket = new Socket(
            AddressFamily.InterNetwork,
            SocketType.Stream,
            ProtocolType.Tcp
        );

        ApplyTcpOptimization(serverSocket);

        // Ví dụ bind & listen (có thể bỏ nếu không cần)
        serverSocket.Bind(new IPEndPoint(IPAddress.Any, 9000));
        serverSocket.Listen(10);

        Console.WriteLine("Server socket initialized with TCP optimizations.");

        serverSocket.Close();
    }
}

