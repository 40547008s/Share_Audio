import pyaudio

p = pyaudio.PyAudio()

# 列出所有音频设备
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print(f"Device {i}: {device_info['name']}")

# 配置音频参数
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# 使用适当的设备索引
input_device_index = int(input("选择输入设备索引: "))
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=CHUNK)

print("音频流已打开")

# 接下来是连接到服务器并传输音频数据的代码...
