from machine import I2C
import time, math

class MAX30102:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x57  # Dirección I2C del MAX30102
        self.setup()

    def setup(self):
        # Configuración básica del sensor (modo SpO2)
        self.i2c.writeto_mem(self.addr, 0x09, b'\x03')  # Modo SpO2
        self.i2c.writeto_mem(self.addr, 0x0A, b'\x27')  # Amplitud LED
        self.i2c.writeto_mem(self.addr, 0x0C, b'\x03')  # LED rojo e IR activos

    def read_fifo(self):
        data = self.i2c.readfrom_mem(self.addr, 0x07, 6)
        red = (data[0] << 16 | data[1] << 8 | data[2]) & 0x3FFFF
        ir = (data[3] << 16 | data[4] << 8 | data[5]) & 0x3FFFF
        return red, ir

    def read_sequential(self, samples=50):
        red_buf = []
        ir_buf = []
        for _ in range(samples):
            red, ir = self.read_fifo()
            red_buf.append(red)
            ir_buf.append(ir)
            time.sleep(0.02)
        return red_buf, ir_buf

    def calc_hr_spo2(self, ir_data, red_data):
        # Calcular HR (frecuencia cardíaca) basada en picos
        min_ir = min(ir_data)
        max_ir = max(ir_data)
        threshold = min_ir + 0.6 * (max_ir - min_ir)
        peaks = [i for i in range(1, len(ir_data)-1)
                 if ir_data[i-1] < ir_data[i] > ir_data[i+1] and ir_data[i] > threshold]

        if len(peaks) > 1:
            intervals = [peaks[i+1] - peaks[i] for i in range(len(peaks)-1)]
            avg_interval = sum(intervals) / len(intervals)
            bpm = 60 / (avg_interval * 0.02)  # 0.02s por muestra
        else:
            bpm = 0

        # Calcular SpO2 de manera aproximada
        ir_ac = max_ir - min_ir
        red_ac = max(red_data) - min(red_data)
        ratio = (red_ac / ir_ac) if ir_ac != 0 else 0
        spo2 = 110 - 25 * ratio
        spo2 = max(0, min(spo2, 100))

        return bpm, spo2
