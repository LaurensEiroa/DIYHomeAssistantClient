import gpiozero
import time

class Relay:
    def __init__(self,GPIO_PIN=26,test=False):
        # Create a relay object
        self.relay = gpiozero.OutputDevice(GPIO_PIN, active_high=True, initial_value=False)
        self.relay_status = False
        #self.turn_on_relay()

    def turn_on_relay(self):
        print("Turning on the relay")
        self.relay_status = True
        self.relay.on()

    def turn_off_relay(self):
        print("Turning off the relay")
        self.relay_status = False
        self.relay.off()

    def toggle_relay(self):
        print("Toggling the relay")
        self.relay_status = not self.relay_status
        self.relay.toggle()

    def close_relay(self):
        print("Closing the relay")
        self.relay.close() # release the GPIO pin

    def get_relay_status(self):
        return self.relay_status

    def test_relay(self):
        print("Testing the relay")
        for i in range(2):
            self.turn_on_relay()
            time.sleep(2)
            self.turn_off_relay()
            time.sleep(1)
            self.toggle_relay()
            time.sleep(1)
            self.toggle_relay()
            time.sleep(1)

if __name__ == "__main__":
    lamp = Relay(test=True)
    #lamp.test_relay()
    print("Exiting program")
    # lamp.turn_off_relay()  # Ensure the relay is turned off before exiting
    # lamp.close_relay()  # Release the GPIO pin
    lamp.turn_on_relay()
    time.sleep(3)
    lamp.turn_off_relay()
    time.sleep(3)
