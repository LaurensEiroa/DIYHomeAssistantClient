
import time
import board
import busio
import adafruit_sht31d

def read_data():
    # Create I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create SHT31D sensor object
    sensor = adafruit_sht31d.SHT31D(i2c)
    temperature = sensor.temperature
    humidity = sensor.relative_humidity
    return temperature, humidity

if __name__ == "__main__":
    while True:
        temperature, humidity = read_data()
        print(f"Temperature: {temperature:.2f} C\tHumidity: {humidity:.2f} %")
        time.sleep(5)
