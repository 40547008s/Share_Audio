import socket
import pyaudio

# 配置音频参数
CHUNK = 1024*8*2
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
INPUT_DEVICE_INDEX = 2  # 使用 CABLE Input (VB-Audio Virtual Cable)

# 初始化音频流
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=INPUT_DEVICE_INDEX,
                frames_per_buffer=CHUNK)

# 连接到服务器
server_address = ('192.168.54.103', 7754)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

print("已连接到服务器")

# 传输音频数据
try:
    while True:
        data = stream.read(CHUNK)
        client_socket.sendall(data)
finally:
    # 清理资源
    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()
