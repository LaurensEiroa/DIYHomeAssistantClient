from scr.streamer.picamera.picamera import Camera
from scr.streamer.udp_streamer.udp_sender import UDPSender

async def udp_stream(sender_ip, receiver_ip, port):
    cam = Camera()
    udp_sender = UDPSender(sender_ip, receiver_ip, port=port)
    await cam.stream_udp(udp_sender=udp_sender)