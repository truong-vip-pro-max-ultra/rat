from flask import Flask, Response, render_template
from io import BytesIO
from PIL import ImageGrab
import socket
import threading
from time import sleep

host = ''
port = 9999
data_screen = b''
data_max = 1024*60
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, port))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
# def gen():
#     global data_screen
#     while True:
#         data = b''
#         while True:
#             try:
#                 img_bytes ,address = server.recvfrom(data_max)
#                 if not img_bytes:
#                     break
#                 if img_bytes != b'done': # done
#                     data += img_bytes
#                     server.sendto(b'ok',address) # notify ok
#                 else:
#                     break
#             except:
#                 break
#         data_screen = data
def gen():
    while True:
        data = b''
        while True:
            img_bytes ,address = server.recvfrom(data_max)
            if not img_bytes:
                break
            if img_bytes != b'done': # done
                data += img_bytes
                server.sendto(b'ok',address) # notify ok
            else:
                break
        yield(data)
def thread_gen():
    global data_screen
    while True:
        yield(data_screen)
if __name__ == '__main__':
    # t = threading.Thread(target=gen)
    # t.start()
    app.run(host='0.0.0.0', port=80)
