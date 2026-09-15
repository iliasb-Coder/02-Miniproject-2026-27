from machine import Pin
from time import ticks_ms, ticks_diff

BUTTON1_PIN = 5
BUTTON2_PIN = 6

btn1 = Pin(BUTTON1_PIN, Pin.IN, Pin.PULL_UP)
btn2 = Pin(BUTTON2_PIN, Pin.IN, Pin.PULL_UP)

DEBOUNCE_MS = 200 

# last accepted press time for each button
_last_press = {"btn1": 0, "btn2": 0}
# last raw pin state, used to detect a falling edge (press) in poll()
_last_state = {"btn1": 1, "btn2": 1}


def _debounced(name, now):
    
    if ticks_diff(now, _last_press[name]) >= DEBOUNCE_MS:
        _last_press[name] = now
        return True
    return False



def poll():
    
    now = ticks_ms()
    pressed1 = False
    pressed2 = False

    state1 = btn1.value()
    if _last_state["btn1"] == 1 and state1 == 0:  # falling edge = press
        if _debounced("btn1", now):
            pressed1 = True
    _last_state["btn1"] = state1

    state2 = btn2.value()
    if _last_state["btn2"] == 1 and state2 == 0:
        if _debounced("btn2", now):
            pressed2 = True
    _last_state["btn2"] = state2

    return pressed1, pressed2



    def _irq1(pin):
        now = ticks_ms()
        if _debounced("btn1", now) and on_button1:
            on_button1()

    def _irq2(pin):
        now = ticks_ms()
        if _debounced("btn2", now) and on_button2:
            on_button2()

    btn1.irq(trigger=Pin.IRQ_FALLING, handler=_irq1)
    btn2.irq(trigger=Pin.IRQ_FALLING, handler=_irq2)



if __name__ == "__main__":
    from time import sleep_ms

    print("Press either button (Ctrl-C to stop)...")
    while True:
        p1, p2 = poll()
        if p1:
            print("Button 1 pressed")
        if p2:
            print("Button 2 pressed")
        sleep_ms(10)
