import asyncio
import websockets

from scr.utils.sensors.sht31d.sht31d import read_data
from scr.utils.devices.relay.mechanical_relay import Relay
from scr.utils.picamera.picamera import Camera

class Client:
    def __init__(self, address="0.0.0.0", port="8080"):
        self.address = address
        self.port = port

        # TODO
        self.lamp = Relay(GPIO_PIN=18)
        self.cam = Camera()

        self.stream_task = None
        
    async def start_server(self):
        server = await websockets.serve(lambda ws: self.handler(ws), self.address, self.port)
        print(f"WebSocket server on pi Zero is running on ws://{self.address}:{self.port}")
        await asyncio.Future()  # Run forever

    async def handler(self, websocket):
        print("Client connected")
        async for message in websocket:
            print(f"Received message: {message}")
            answer = await self.message_processor(message)
            await websocket.send(f"Echo: {answer}")

    async def message_processor(self, message):
        match message:
            # Sensor Readings
            case "read_sht31d":
                temp, hum = read_data()
                return f"Temperature: {temp} - Humidity: {hum}"
            
            # Light Control
            case "turn_on_relay":
                self.lamp.turn_on_relay()
                return "relay_on"
            case "turn_off_relay":
                self.lamp.turn_off_relay()
                return "relay_off"
            case "toggle_relay":
                self.lamp.toggle_relay()
                return "relay_toggled"
            
            # Stream Control
            case "start_http_stream":
                self.cam.start_streaming()
                self.stream_task = asyncio.create_task(self.cam.stream_http())
                return "streaming started"
            case "stop_http_stream":
                if self.cam.streaming:
                    self.cam.stop_streaming()
                if self.stream_task:
                    self.stream_task.cancel()
                    self.stream_task = None
                return "stream stopped"
            case "start_udp_stream":
                pass
            case "stop_udp_stream":
                pass

if __name__ == "__main__":
    cli = Client()
    asyncio.run(cli.start_server())
