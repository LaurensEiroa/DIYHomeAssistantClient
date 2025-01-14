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

if __name__=="__main__":
    # Capture video from the default camera
    sender_ip = '192.168.1.1'  # Replace with your sender IP address
    receiver_ip = '192.168.1.2'  # Replace with your receiver IP address
    port = 12345  # Replace with your desired port number

    udp_sender = UDPSender(sender_ip, receiver_ip, port)


    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Send the frame
        udp_sender.send_frame(frame)

        # Display the frame (optional)
        cv2.imshow('Frame', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    pass