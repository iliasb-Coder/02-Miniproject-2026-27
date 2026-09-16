from machine import Pin, PWM
from time import ticks_ms, ticks_diff, sleep_ms

# assuming LEDs: red = GPIO 7, blue = GPIO 8, green = GPIO 9
red = PWM(Pin(7), freq=1000, duty_u16=0)
blue = PWM(Pin(8), freq=1000, duty_u16=0)
green = PWM(Pin(9), freq=1000, duty_u16=0)

def all_off():
    red.duty_u16(0)
    blue.duty_u16(0)
    green.duty_u16(0)

def turn_on(led):
    all_off()
    led.duty_u16(65535)
    
def pulse(led, elapsed_ms):
    phase = elapsed_ms % 1000
    if phase < 500:
        brightness = phase * 65535 // 500
    else:
        brightness = (1000 - phase) * 65535 // 500
    led.duty_u16(brightness)
    
# test that pulses red LED three times
if __name__ == "__main__":
    all_off()
    start = ticks_ms()
    try:
        while True:
            elapsed = ticks_diff(ticks_ms(), start)
            if elapsed >= 3000:
                break
            pulse(red, elapsed)
            sleep_ms(10)
    finally:
        all_off()