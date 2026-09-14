from machine import Pin
from time import sleep_ms

coils = [Pin(pin, Pin.OUT) for pin in (1, 2, 3, 4)]

for coil in coils:
    coil.off()

phase = 3


def move(steps, direction=1):
    global phase

    for _ in range(steps):
        phase = (phase + direction) % 4

        for i, coil in enumerate(coils):
            coil.value(i == phase)

        sleep_ms(4)

    for coil in coils:
        coil.off()


move(200, 1)
sleep_ms(1000)
move(200, -1)