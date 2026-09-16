import stepper
import timer_logic
import button
import led

from time import ticks_ms, ticks_diff, sleep_ms

STEPS_PER_REV = 2048
SECONDS_PER_REV = 30

start_time = 0
total_time_ms = 0
start_position = 0
last_position = 0


def return_to_origin():
    global last_position

    if last_position > 0:
        stepper.move(last_position, -1)

    last_position = 0


while True:

    button1, button2 = button.poll()

    # Cycle preset
    if button1 and not timer_logic.running:
        selected = timer_logic.next_preset()
        print("Preset:", selected, "seconds")
        led.turn_on(led.green)

    # Start timer
    if button2 and not timer_logic.running:

        return_to_origin()

        selected = timer_logic.current_preset()

        total_time_ms = selected * 1000

        start_position = int(
            STEPS_PER_REV * selected / SECONDS_PER_REV
        )

        stepper.move(start_position, 1)
        last_position = start_position

        timer_logic.start_timer()
        start_time = ticks_ms()

        print("Timer started:", selected, "seconds")

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

        if remaining == 0:

            return_to_origin()

            timer_logic.stop_timer()

            led.turn_on(led.red)

            print("Time is up!")

    sleep_ms(10)