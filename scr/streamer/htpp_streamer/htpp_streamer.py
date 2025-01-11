import cv2
import asyncio
from utils import HTTPStreamer

class Camera:
    def __init__(self, resolution=(640, 480)):
        self.camera = None
        self.streaming = False
        self.resolution = resolution
        self.init_camera()

    def init_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

    async def send_frame_http(self, http_streamer):
        while self.streaming:
            ret, frame = self.camera.read()
            if ret:
                await http_streamer.send_frame(frame)
            await asyncio.sleep(0.01)  # Small delay to prevent high CPU usage

    def start_streaming(self):
        self.streaming = True

    def stop_streaming(self):
        self.streaming = False
        self.camera.release()



# Example usage
if __name__ == "__main__":
    print("creating camera")
    camera = Camera(resolution=(1280,720))
    print("creating http streamer")
    http_streamer = HTTPStreamer()
    
    # Start the HTTP server
    import threading
    print("creating new thread")
    server_thread = threading.Thread(target=http_streamer.start)
    print("starting thread")
    server_thread.start()
    
    # Start streaming
    print("starting the stream")
    camera.start_streaming()
    print("sending frames")
    asyncio.run(camera.send_frame_http(http_streamer))
