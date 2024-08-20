import pyaudio

p = pyaudio.PyAudio()

# 列出所有设备
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']} - {info['maxInputChannels']} 输入通道")

p.terminate()
