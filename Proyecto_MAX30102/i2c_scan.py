from machine import Pin, I2C
import time

# Configura el bus I2C (SDA=GPIO8, SCL=GPIO9)
i2c = I2C(0, scl=Pin(9), sda=Pin(8))

print("\n🔍 Escaneando bus I2C...\n")
time.sleep(1)

devices = i2c.scan()

if len(devices) == 0:
    print("⚠️  No se detectaron dispositivos I2C.")
    print("➡️  Verifica las conexiones SDA/SCL, VCC y GND.")
else:
    print("✅ Dispositivos detectados en el bus I2C:")
    for d in devices:
        print(" - Dirección:", hex(d))
