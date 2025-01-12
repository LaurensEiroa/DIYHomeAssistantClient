import Adafruit_BMP.BMP180 as BMP180


def read_data():
    # Create an instance of the BMP180 sensor
    sensor = BMP180.BMP180()
    # Read temperature, pressure, and altitude
    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()

    return temperature, pressure, altitude

# Example usage
if __name__ == "__main__":
    temp, pres, alt = read_data()
    print(f"Temperature: {temp:.2f} C")
    print(f"Pressure: {pres / 100.0:.2f} hPa")
    print(f"Altitude: {alt:.2f} m")
