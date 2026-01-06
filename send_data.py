import os
from dotenv import load_dotenv
import requests
import random
import time
from dataclasses import dataclass

load_dotenv()

try:
    if os.getenv("N8N_DEBUG") == "TRUE":
        n8n_url = os.getenv("N8N_WEBHOOK_TEST_URL")
    else:
        n8n_url = os.getenv("N8N_WEBHOOK_PROD_URL")
except ValueError:
    raise ValueError("In case of fuckup...")

@dataclass
class Payload:
    """
    Data payload for sensor readings.
    param temperature: Temperature reading from the sensor.
    param humidity: Humidity reading from the sensor.
    param device: Identifier for the device sending the data.
    """
    temperature: int
    humidity: int
    device: str = "PC-SENSOR-01"

def generate_payload()-> Payload:
    """
    Generate a random payload for sensor data.
    return: Payload object with random temperature and humidity values.
    """
    temperature = random.randint(20, 40)
    humidity = random.randint(30, 80)
    return Payload(temperature, humidity)

def send_payload(payload: Payload)-> None:
    """
    Send the payload to the n8n webhook URL.
    param payload: Payload object containing sensor data.
    return: None
    """
    try:
        response = requests.post(n8n_url, json=(payload.__dict__))
        response.raise_for_status()
        print(f"Payload sent successfully: {payload}")
    except requests.RequestException as e:
        print(f"Failed to send payload: {e}")

while True:
    payload = generate_payload()
    send_payload(payload)
    time.sleep(10)