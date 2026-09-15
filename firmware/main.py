import stepper
import timer_logic
import button
import led

from time import ticks_ms, ticks_diff, sleep_ms

STEPS_FOR_30_MIN = 600

start_time = 0
total_time_ms = 0
start_position = 0
last_position = 0

while True:

    button1, button2 = button.poll()

    # Cycle preset
    if button1 and not timer_logic.running:
        selected = timer_logic.next_preset()
        print("Preset:", selected, "minutes")
        led.turn_on(led.green)

    # Start timer
    if button2 and not timer_logic.running:
        selected = timer_logic.current_preset()

        timer_logic.start_timer()

        total_time_ms = selected * 60 * 1000
        start_time = ticks_ms()

        start_position = int(
            STEPS_FOR_30_MIN * selected / 30
        )

        last_position = start_position

        stepper.move(start_position, 1)

        print("Timer started")

    if timer_logic.running:

        elapsed = ticks_diff(ticks_ms(), start_time)

        led.pulse(led.blue, elapsed)

        remaining = total_time_ms - elapsed

        if remaining < 0:
            remaining = 0

        target_position = int(
            start_position * remaining / total_time_ms
        )

        steps_to_move = last_position - target_position

        if steps_to_move > 0:
            stepper.move(steps_to_move, -1)
            last_position = target_position

        # Timer finished
        if remaining == 0:
            timer_logic.stop_timer()
            led.turn_on(led.red)
            print("Time is up!")

    sleep_ms(10)