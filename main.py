import asyncio
# Example usage
if __name__ == "__main__":
    #from scr.utils.picamera.picamera import test_camera_http_streamer
    #asyncio.run(test_camera_http_streamer())

    from scr.websocket.websocket_client import Client
    cli = Client()
    asyncio.run(cli.start_server())