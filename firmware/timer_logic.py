preset = [15, 20, 25, 30]
preset_index = 0
running = False


def current_preset():
    
    return preset[preset_index]

def next_preset():
    
    global preset_index
    
    preset_index = (preset_index + 1) % len(preset)
    
    return current_preset()


def start_timer():
    
    global running
    
    running = True


def stop_timer():
    
    global running
    
    running = False


def reset_timer():
    
    global running, preset_index
    
    running = False
    
    preset_index = 0
