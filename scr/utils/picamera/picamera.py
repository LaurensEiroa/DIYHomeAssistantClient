import picamera2
import asyncio

class Camera:
    def __init__(self, resolution=(640, 480), format='XRGB8888'):
        self.camera = None
        self.streaming = False
        self.resolution = resolution
        self.format = format
        self.init_camera()

    def init_camera(self):
        self.camera = picamera2.Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"format": self.format, "size": self.resolution}))

    def start_streaming(self):
        self.streaming = True
        self.camera.start()

    def stop_streaming(self):
        self.streaming = False
        self.camera.stop()

    async def stream_udp(self, udp_sender):
        while self.streaming:
            frame = self.camera.capture_array()
            udp_sender.send_frame(frame)
            await asyncio.sleep(0)  # Yield control to the event loop

    async def stream_http(self, http_streamer):
        while self.streaming:
            frame = self.camera.capture_array()
            http_streamer.send_frame(frame)
            await asyncio.sleep(0)  # Yield control to the event loop

def test_camera_http_streamer():
    from scr.streamer.htpp_streamer.htpp_streamer import HTTPStreamer
    print("creating camera")
    camera = Camera()#resolution=(1280, 720))
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
    asyncio.run(camera.stream_http(http_streamer))
    print("stopping the stream")
    camera.stop_streaming()

# Example usage
if __name__ == "__main__":
    test_camera_http_streamer()
