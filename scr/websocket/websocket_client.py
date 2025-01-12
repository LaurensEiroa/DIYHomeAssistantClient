
import asyncio
import websockets
from scr.utils.devices.relay.control_relay import Relay
from scr.utils.sensors.sht31_d.read_sht31d_zero import read_data

from scr.streamer.htpp_streamer.htpp_streamer import HTTPStreamer

def message_processor(lamp, message):
    match message:
        case "read_sht31d":
            temp, hum = read_data()
            return f"Temperature: {temp} - Humidity: {hum}"
        case "turn_on_relay":
            lamp.turn_on_relay()
            return "relay_on"
        case "turn_off_relay":
            lamp.turn_off_relay()
            return "relay_off"
        case "toggle_relay":
            lamp.toggle_relay()
            return "relay_toggled"
        case "start_http_stream":
            pass
        case "stop_http_stream":
            pass
        case "start_udp_stream":
            pass
        case "stop_udp_stream":
            pass

async def handler(websocket, lamp):
    print("Client connected")
    async for message in websocket:
        print(f"Received message: {message}")
        answer = message_processor(lamp, message)
        await websocket.send(f"Echo: {answer}")

async def main():
    address = "0.0.0.0"
    port = 8080
    lamp = Relay(GPIO_PIN=26)  # Create the relay object here
    start_server = websockets.serve(lambda ws: handler(ws, lamp), address, port)
    await start_server
    print(f"WebSocket server on pi Zero is running on ws://{address}:{port}")
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
