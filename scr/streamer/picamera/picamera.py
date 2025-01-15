import picamera2
import asyncio

from scr.streamer.htpp_streamer.htpp_streamer import HTTPStreamer

class Camera:
    def __init__(self, resolution=(640, 480), format='XRGB8888'):
        self.camera = None
        self.streaming = False
        self.resolution = resolution
        self.format = format
        self.http_streamer = None
        self.init_camera()

    def init_camera(self):
        self.camera = picamera2.Picamera2()
        self.camera.configure(self.camera.create_video_configuration(main={"format": self.format, "size": self.resolution}))

    def start_streaming(self):
        self.streaming = True
        self.camera.start()
        print("creating http streamer")
        self.http_streamer = HTTPStreamer()

    def stop_streaming(self):
        self.streaming = False
        self.camera.stop()
        if self.http_streamer:
            self.http_streamer.stop()

    async def stream_udp(self, udp_sender):
        while self.streaming:
            frame = self.camera.capture_array()
            await udp_sender.send_frame(frame)
            await asyncio.sleep(0)  # Yield control to the event loop

    async def stream_http(self):
        # Start the HTTP server
        print("starting HTTP server")
        loop = asyncio.get_event_loop()
        server = loop.run_in_executor(None, self.http_streamer.start)

        while self.streaming:
            frame = self.camera.capture_array()
            await self.http_streamer.send_frame(frame)
            await asyncio.sleep(0)  # Yield control to the event loop
        await server

async def test_camera_http_streamer():
    print("creating camera")
    camera = Camera()#resolution=(1280, 720))    
    # Start streaming
    print("starting the stream")
    camera.start_streaming()
    print("sending frames")
    await camera.stream_http()
    print("stopping the stream")
    camera.stop_streaming()

# Example usage
if __name__ == "__main__":
    asyncio.run(test_camera_http_streamer())
