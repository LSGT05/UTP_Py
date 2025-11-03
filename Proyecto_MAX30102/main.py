from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import max30102
import time

# --- Inicialización I2C ---
i2c = I2C(0, scl=Pin(9), sda=Pin(8))

# --- Inicializar pantalla OLED ---
oled = SSD1306_I2C(128, 64, i2c)

# --- Inicializar sensor MAX30102 ---
sensor = max30102.MAX30102(i2c=i2c)

# --- Mostrar mensaje inicial ---
oled.fill(0)
oled.text("MAX30102 Sensor", 0, 0)
oled.text("Iniciando...", 0, 20)
oled.show()
time.sleep(2)

# --- Loop principal ---
while True:
    # Leer datos crudos del sensor
    red, ir = sensor.read_sequential()

    if len(red) > 0 and len(ir) > 0:
        # Calcular BPM y SpO2
        bpm, spo2 = sensor.calc_hr_spo2(ir, red)

        # Mostrar en consola (para depuración)
        print("BPM:", bpm, "SpO2:", spo2)

        # Mostrar en pantalla OLED
        oled.fill(0)
        oled.text("Frecuencia Card:", 0, 0)
        oled.text("{:.1f} BPM".format(bpm if bpm else 0), 0, 20)
        oled.text("Oxigeno:", 0, 40)
        oled.text("{:.1f} %".format(spo2 if spo2 else 0), 0, 55)
        oled.show()

    else:
        oled.fill(0)
        oled.text("Coloca el dedo", 0, 30)
        oled.show()

    time.sleep(1)
