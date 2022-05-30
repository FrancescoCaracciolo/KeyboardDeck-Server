from pynput import keyboard

from KeyboardDeck.network import NetworkManager



def on_press(key, network: NetworkManager, controlOn: int):
    """Does necessary actions when a key is pressed

    Args:
        key (keyboardlistener key): The key pressed by the user
        network (NetworkManager): NetworkManager object to send the requests
        controlOn (int): If the modkey is on, not implemented yet
    """
    try:
        print('{0}'.format(
            key.char))
        network.send_keypress("a") # Temporary, str(key.char) to get the right key
        if controlOn % 2 == 1:  # One day it will be useful
            pass
    except AttributeError:
        if (key == keyboard.Key.ctrl):
            controlOn += 1
        print('[{0}]'.format(
            key))

def on_release(key, controlOn: int):
    """When a key is released, not implemented yet

    Args:
        key (_type_): The key pressed
        controlOn (int): Not implemented yet
    """
    try:
        key.char
    except AttributeError:
        if (key == keyboard.Key.ctrl):
            controlOn += 1