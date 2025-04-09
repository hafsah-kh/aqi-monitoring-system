import time
import serial
from azure.iot.device import IoTHubDeviceClient, Message


CONNECTION_STRING = "HostName=iotc-abe5e1ae-3371-4bb7-a87c-75fb736060f4.azure-devices.net;DeviceId=arduino---mq-135;SharedAccessKey=l6BqlgYLbj+1WSKiK6SjR1d+9MOQOOLJgn37VwOG5q4="


SERIAL_PORT = "COM7"  
BAUD_RATE = 9600


MESSAGE_TEMPLATE = '{{"airQuality": {}}}'

client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def send_air_quality_data():
    """Read air quality data from Arduino and send it to Azure IoT Hub."""
    while True:
        if ser.in_waiting:
            try:
                sensor_value = ser.readline().decode("utf-8").strip()
                if sensor_value.isdigit(): 
                    air_quality = int(sensor_value)
                    message = Message(MESSAGE_TEMPLATE.format(air_quality))
                    print(f"Sending message: {message}")
                    client.send_message(message)
                    print("Message successfully sent to Azure IoT Hub.")
                else:
                    print("Invalid sensor data received:", sensor_value)
            except Exception as e:
                print("Error reading from serial:", e)

        time.sleep(5)  


try:
    print("Connecting to Azure IoT Hub...")
    client.connect()
    print("Connected successfully.")
    send_air_quality_data()
except Exception as e:
    print("Connection error:", e)
finally:
    client.shutdown()
    ser.close()
