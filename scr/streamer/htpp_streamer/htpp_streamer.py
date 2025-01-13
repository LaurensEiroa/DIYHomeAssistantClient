# HTTPStreamer class
import cv2
from flask import Flask, Response

class HTTPStreamer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.app = None
        self.frame = None

    # This function will stream the self.frames to the web app
    def generate(self):
        while True:
            if self.frame is not None:
                ret, jpeg = cv2.imencode('.jpg', self.frame)
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    # This function will recieve the frame coming from the camera
    async def send_frame(self, frame):
        self.frame = frame

    def start(self):
        self.app = Flask(__name__)
        
        @self.app.route('/')
        def video_feed():
            return Response(self.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

        self.app.run(host=self.host, port=self.port)

    def stop(self):
        del self.app
        self.app = None

