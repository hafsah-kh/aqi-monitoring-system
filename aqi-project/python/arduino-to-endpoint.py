import serial
import requests
import json
from datetime import datetime
from time import sleep

# Arduino Serial Configuration
ARDUINO_PORT = 'COM7'  # Change to your Arduino's port
BAUD_RATE = 9600
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)

# Azure ML Endpoint Configuration
ML_ENDPOINT_URL = "https://aqi-ml-endpoint.eastus.inference.ml.azure.com/score"  
API_KEY = "9l1ws3mYkajBgOBstJGi62WBytVvIEMSurbnxS0l1UZVfJOLpllIJQQJ99BDAAAAAAAAAAAAINFRAZML3V8W"

def send_to_ml_endpoint(sensor_data):
    """Send sensor data to Azure ML endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
      "input_data": {
        "columns": [
          "created_at",
          "entry_id",
          "field1",
          "field2",
          "field3",
          "field4",
          "field5",
          "field6",
          "field7"
        ],
        "index": [0, 1, 2, 3],
        "data": [
          [
            "2024-04-06 12:00:27",
            1256,
            163,
            33.8,
            32.0,
            49.0,
            520.0,
            18.0,
            21.0
          ],
          [
            "2024-04-06 12:15:27",
            1256,
            163,
            None,
            32.0,
            49.0,
            520.0,
            18.0,
            21.0
          ],
          [
            "2024-04-06 12:30:27",
            1256,
            163,
            None,
            32.0,
            49.0,
            520.0,
            18.0,
            21.0
          ],
          [
            "2024-04-06 12:45:27",
            1256,
            163,
            None,
            32.0,
            49.0,
            520.0,
            18.0,
            21.0
          ]
        ]
      }
    }

    
    try:
        response = requests.post(ML_ENDPOINT_URL, headers=headers, json=payload)
        if response.status_code == 200:
            prediction = response.json()
            print(f"Prediction: {prediction}")
            return prediction
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Request failed: {str(e)}")

def read_arduino_data():
    """Read and parse data from Arduino"""
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:  # Check if data was received
                try:
                    aqi_value = float(line)
                    print(f"Raw AQI: {aqi_value}")
                    return aqi_value
                except ValueError:
                    print(f"Invalid data: {line}")
        except Exception as e:
            print(f"Serial error: {str(e)}")
        sleep(0.1)

if __name__ == "__main__":
    try:
        print("Starting Arduino-Azure ML integration...")
        while True:
            # 1. Read from Arduino
            aqi = read_arduino_data()
            
            # 2. Send to ML Endpoint
            if aqi is not None:
                prediction = send_to_ml_endpoint(aqi)
                
                # (Optional) Send prediction back to Arduino
                # ser.write(f"PRED:{prediction}\n".encode())
            
            sleep(5)  # Match your Arduino's delay
            
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        ser.close()
