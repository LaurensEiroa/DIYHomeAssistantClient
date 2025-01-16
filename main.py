from scr.streamer.stream import udp_stream
from scr.websocket.websocket_client import Client
from config import Config

import asyncio


async def run_udp():
    await udp_stream(sender_ip=Config.IPs["piZero1"],receiver_ip=Config.IPs["pi5"],port= Config.UDP_PORT)

async def run_websocket():
    cli = Client()
    await cli.start_server()

async def run_all():
    await asyncio.gather(
        run_udp(),
        run_websocket()
    )

if __name__ == "__main__":
    asyncio.run(run_all())
    
