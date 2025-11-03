import network
import socket
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import max30102

# --- CONFIGURACIÓN I2C ---
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)
sensor = max30102.MAX30102(i2c=i2c)

# --- CONECTAR A WI-FI ---
SSID = "TU_RED_WIFI"
PASSWORD = "TU_CONTRASENA_WIFI"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando a Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print("\n Conectado a Wi-Fi:", wlan.ifconfig())
    return wlan

wlan = conectar_wifi()

# --- CREAR SERVIDOR WEB ---
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print(" Servidor web iniciado en:", wlan.ifconfig()[0])

# --- VARIABLES GLOBALES ---
bpm = 0
spo2 = 0

def generar_pagina(bpm, spo2):
    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="2">
        <title>MAX30102 Monitor</title>
        <style>
            body {{ font-family: Arial; text-align:center; background:#111; color:#0f0; }}
            h1 {{ color:#0ff; }}
            .valor {{ font-size:48px; }}
        </style>
    </head>
    <body>
        <h1>Monitor MAX30102</h1>
        <p>BPM</p>
        <div class="valor">{bpm:.1f}</div>
        <p>SpO₂</p>
        <div class="valor">{spo2:.1f}%</div>
        <p><small>Actualiza cada 2 segundos</small></p>
    </body>
    </html>
    """
    return html

# --- BUCLE PRINCIPAL ---
while True:
    red, ir = sensor.read_sequential()
    if len(red) > 0 and len(ir) > 0:
        bpm, spo2 = sensor.calc_hr_spo2(ir, red)
        print("BPM:", bpm, "SpO2:", spo2)

        # Mostrar en OLED
        oled.fill(0)
        oled.text("BPM:{:.1f}".format(bpm), 0, 10)
        oled.text("SpO2:{:.1f}%".format(spo2), 0, 30)
        oled.show()

    # Aceptar cliente web
    try:
        cl, addr = s.accept()
        request = cl.recv(1024)
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(generar_pagina(bpm, spo2))
        cl.close()
    except:
        pass

    time.sleep(1)
