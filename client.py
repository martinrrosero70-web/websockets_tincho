import network
import time
from machine import Pin, ADC
import usocket as socket
import ustruct as struct

SSID = "TU_WIFI"
PASSWORD = "TU_PASWORD"
SERVER_IP = "186.4.129.103"
SERVER_PORT = 8765

def connect_wiffi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("Conectado a WiFi...")
        time.sleep(1)
    print("Conectado:", wlan.ifconfig())    

led = Pin(2, Pin.OUT)
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

from uwebsockets.client import connect

connect_wiffi()

try:
    with connect(f"ws//{SERVER_IP}:{SERVER_PORT}") as ws:
        print("Conectado al servidor NiceGui")
        while True:
            val = pot.read()
            ws.send(str(val))

            try:
                msg = ws.recv()
                if msg == "ON":
                    led.value(1)
                elif msg == "OFF":
                    led.value(0)
            except:
                pass 

            time.sleep(0.1)
except Exception as e:
    print("error:", e)                        