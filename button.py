"""
button.py — tactile switch input for the meeting timer

Hardware assumption (per hookup table):
    Button 1 -> GPIO5
    Button 2 -> GPIO6
    Each switch wired between the GPIO pin and GND, using the
    ESP32-S3's internal pull-up, so the pin reads HIGH (1) when
    not pressed and LOW (0) when pressed.

Two ways to use this module:
  1. Polling  -> call poll() once per loop iteration; it returns
     which button(s), if any, were just pressed this cycle.
  2. Interrupts -> call attach_irq(cb1, cb2) once at startup and
     your callbacks fire automatically on a press.

Both paths share the same debounce logic so you don't get
multiple triggers from one physical press.
"""

from machine import Pin
from time import ticks_ms, ticks_diff

# --- pin setup -------------------------------------------------
BUTTON1_PIN = 5
BUTTON2_PIN = 6

btn1 = Pin(BUTTON1_PIN, Pin.IN, Pin.PULL_UP)
btn2 = Pin(BUTTON2_PIN, Pin.IN, Pin.PULL_UP)

DEBOUNCE_MS = 200  # ignore edges closer together than this

# last accepted press time for each button
_last_press = {"btn1": 0, "btn2": 0}
# last raw pin state, used to detect a falling edge (press) in poll()
_last_state = {"btn1": 1, "btn2": 1}


def _debounced(name, now):
    """Return True if enough time has passed since the last accepted
    press of this button to treat this as a new, real press."""
    if ticks_diff(now, _last_press[name]) >= DEBOUNCE_MS:
        _last_press[name] = now
        return True
    return False


# --- polling API -------------------------------------------------
def poll():
    """
    Call this once per loop iteration (no sleep longer than ~20ms
    between calls, or you may miss a quick press).

    Returns a tuple (pressed1, pressed2) of booleans, True only on
    the loop iteration where a debounced press is detected.
    """
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


# --- interrupt-driven API -----------------------------------------
def attach_irq(on_button1=None, on_button2=None):
    """
    Attach debounced interrupt handlers. Each callback is called
    with no arguments when its button is pressed.

        def handle_preset():
            print("button 1 pressed")

        def handle_start_stop():
            print("button 2 pressed")

        attach_irq(handle_preset, handle_start_stop)
    """

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


# --- quick manual test ---------------------------------------------
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
