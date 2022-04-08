from pynput import keyboard

count = 0

def on_press(key):
    global count

    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['up', 'down', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        count = count + 1
        print('integer: ' + str(count))
        print('Key pressed: ' + k)

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys









