import socket
import cv2

MAX_DGRAM = 2**15  # Reduce the size to 32,768 bytes

class UDPSender:
    def __init__(self, sender_ip, receiver_ip, port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.bind((sender_ip, port))
        self.receiver_address = (receiver_ip, port)

    def send_frame(self, frame):
        encoded, buffer = cv2.imencode('.jpg', frame)
        buffer = buffer.tobytes()
        size = len(buffer)
        for i in range(0, size, MAX_DGRAM):
            self.server_socket.sendto(buffer[i:i+MAX_DGRAM], self.receiver_address)
