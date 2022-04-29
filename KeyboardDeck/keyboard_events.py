import json
from pynput import keyboard



def on_press(key, network, controlOn):

    try:
        print('{0}'.format(
            key.char))
        message = {
            "request": "send",
            "event": str(key.char),
        }
        message = json.dumps(message)
        network.sendUDP(message)
        if controlOn % 2 == 1:
            pass
    except AttributeError:
        if (key == keyboard.Key.ctrl):
            controlOn += 1
        print('[{0}]'.format(
            key))

def on_release(key, network, controlOn):

    try:
        key.char
    except AttributeError:
        if (key == keyboard.Key.ctrl):
            controlOn += 1