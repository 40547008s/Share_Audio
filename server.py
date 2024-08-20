import socket
import pyaudio
import threading
import time

# 配置音频播放参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
OUTPUT_DEVICE_INDEX = 1  # 使用 Device 1: 喇叭 (Realtek(R) Audio)

# 初始化 PyAudio
p = pyaudio.PyAudio()

# 当前连接和锁
current_conn = None
conn_lock = threading.Lock()  # 保护当前连接的锁

# 打开音频流的函数
def open_audio_stream():
    try:
        return p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      output=True,
                      output_device_index=OUTPUT_DEVICE_INDEX,
                      frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"初始化音频流失败: {e}")
        return None

# 处理客户端连接
def handle_client(conn):
    global current_conn
    with conn_lock:
        # 如果当前有连接，断开旧连接
        if current_conn:
            print("断开旧客户端连接")
            current_conn.close()
        # 更新当前连接
        current_conn = conn
    print("新客户端连接")

    stream = None
    try:
        # 尝试打开音频流
        stream = open_audio_stream()
        if stream is None:
            print("无法打开音频流")
            return

        while True:
            data = conn.recv(CHUNK)
            if not data:
                break
            try:
                stream.write(data)
            except OSError as e:
                print(f"音频流出错: {e}")
                break
    finally:
        with conn_lock:
            print("客户端断开连接")
            if current_conn == conn:
                current_conn = None
        if stream:
            stream.stop_stream()
            stream.close()
        conn.close()

# 主循环，处理连接请求
def server_loop():
    # 建立伺服器socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 7754))  # 绑定伺服器IP和端口
    server_socket.listen(1)  # 只允许一个连接

    print("伺服器已启动，等待客户端连接...")

    try:
        while True:
            conn, addr = server_socket.accept()
            # 使用线程处理客户端连接
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()
    finally:
        server_socket.close()

# 主程序入口
if __name__ == "__main__":
    try:
        server_loop()
    finally:
        p.terminate()
