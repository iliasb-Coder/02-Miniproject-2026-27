from machine import Pin, ADC
from time import sleep

out_pin = Pin(9, Pin.OUT)
adc = ADC(Pin(8))

out_pin.value(1)   # GPIO9 HIGH

while True:
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535

    print("ADC raw:", raw, "Voltage:", voltage, "V")
    sleep(0.5)