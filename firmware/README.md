# Firmware

The `firmware` folder contains the MicroPython code used to control the meeting timer on the XIAO ESP32-S3. The software is split into separate modules so each part of the system can be developed and tested independently before being integrated into `main.py`.

- `stepper.py` controls the 28BYJ-48 stepper motor through the L293D driver using GPIO1–GPIO4.
- `timer_logic.py` manages the timer presets (15, 20, 25, and 30 minutes) and basic timer state.
- `led.py` controls the red, blue, and green LEDs on GPIO7–GPIO9, including PWM pulsing.
- `buttons.py` reads the two push buttons used to control the timer.
- `main.py` integrates the individual modules and runs the complete meeting timer.
