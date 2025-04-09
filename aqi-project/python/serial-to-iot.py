import serial
import time
from azure.iot.device import IoTHubDeviceClient

# Azure IoT Hub connection string
CONNECTION_STRING = "HostName=iotc-abe5e1ae-3371-4bb7-a87c-75fb736060f4.azure-devices.net;DeviceId=arduino---mq-135;SharedAccessKey=l6BqlgYLbj+1WSKiK6SjR1d+9MOQOOLJgn37VwOG5q4="

# Serial port configuration (adjust to match your setup)
SERIAL_PORT = 'COM7'  # Change this to your Arduino's COM port
BAUD_RATE = 9600
TIMEOUT = 1

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def read_arduino_data(ser):
    """Read data from Arduino serial port"""
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("Air Quality Index: "):
            sensor_value = line.split(": ")[1]
            return float(sensor_value)
        return None
    except Exception as e:
        print(f"Error reading serial data: {e}")
        return None

def send_to_iot_hub(client, sensor_value):
    """Send sensor data to Azure IoT Central"""
    try:
        message = {"air_quality": sensor_value}
        client.send_message(str(message))
        print(f"Message sent to IoT Hub: {message}")
    except Exception as e:
        print(f"Error sending message to IoT Central: {e}")

def main():
    # Initialize IoT Central client
    client = iothub_client_init()
    
    # Initialize serial connection
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        time.sleep(2)  # Wait for serial connection to establish
        print(f"Connected to Arduino on {SERIAL_PORT}")
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        return
    
    try:
        while True:
            # Read data from Arduino
            sensor_value = read_arduino_data(ser)
            
            if sensor_value is not None:
                print(f"Air Quality Index: {sensor_value}")
                
                # Send data to IoT Hub
                send_to_iot_hub(client, sensor_value)
            
            # Wait for next reading (matches Arduino's 5-second delay)
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        ser.close()
        client.shutdown()

if __name__ == '__main__':
    main()
