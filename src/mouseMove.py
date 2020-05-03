# # import pyautogui
# # pyautogui.moveTo(100, 150)
# # pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
# # pyautogui.dragTo(100, 150)
# # pyautogui.dragRel(0, 10)  # drag mouse 10 pixels down

# # key

# from pynput.keyboard import Key, KeyCode, Controller, Listener
# import pyautogui as pg
# import time
# import threading


# # def addKey(keyPressed, keyCombinations, currentlyPressedKeys, callback):
# #     if any([keyPressed in combo for combo in keyCombination]):
# #         currentlyPressedKeys.add(keyPressed)
# #         if any(all(k in currentlyPressedKeys for k in combo) for combo in keyCombination):
# #             callback()


# # def removeKey(keyPressed, keyCombinations, currentlyPressedKeys):
# #     if any([keyPressed in combo for combo in keyCombination]):
# #         currentlyPressedKeys.remove(keyPressed)

# pg.FAILSAFE = False
# # kb = Controller()
# # time.sleep(1)
# threadExitFlag = threading.Event()
# threadVar = None
# keyCombination = {Key.ctrl, KeyCode(char='m')}
# direction = True


# def mouse_move_thread(threadExitFlag, distance=10, sleepTime=10):
#     global direction
#     while not threadExitFlag.is_set():
#         if(direction is True):
#             pg.moveRel(distance, 0, duration=0.2)
#             direction = False
#         else:
#             pg.moveRel(-distance, 0, duration=0.2)
#             direction = True
#         time.sleep(sleepTime)


# def on_press(key):
#     global threadExitFlag

#     if key == Key.space:
#         threadVar = threading.Thread(target=mouse_move_thread, args=[
#                                      threadExitFlag]).start()
#     if key == Key.enter:
#         threadExitFlag.set()

#     # Turns this macro back on
#     elif key == Key.esc:
#         if threadExitFlag.is_set():
#             threadExitFlag.clear()


# if __name__ == "__main__":
#     # pg.FAILSAFE = True
#     # # kb = Controller()
#     # # time.sleep(1)
#     # threadExitFlag = threading.Event()
#     # threadVar = None
#     # keyCombination = {Key.ctrl, KeyCode(char='m')}

#     with Listener(on_press=on_press, args=[]) as listener:
#         listener.join()

# # import time
# # from random import randrange


# # def timer():
# #     get_time = int(time.time())
# #     return get_time


# # def main():

# #     while True:
# #         snapshot = {"time": timer(), "position": pg.position()}
# #         time.sleep(5)
# #         if snapshot["position"] == pg.position():
# #             pg.moveTo(400, randrange(1, 50))
# #         else:
# #             pass


# import time
# from pynput.mouse import Button, Controller
# mouseController = Controller()


# def moveMouse(x, y, duration=0.2):
#     sleepBetweenSteps = 0.05
#     stepsNumber = int(duration/sleepBetweenSteps)
#     stepX = int(x/stepsNumber)
#     stepY = int(y/stepsNumber)
#     startX, startY = mouseController.position

#     for step in range(stepsNumber):
#         mouseController.move(stepX, stepY)
#         currentX, currentY = mouseController.position
#         if(currentX == startX or currentX == startY):
#             return
#         time.sleep(sleepBetweenSteps)


# moveMouse(1000, 1000)
# from pynput import keyboard

# # The key combination to check
# # COMBINATION = {keyboard.KeyCode(char='a'), keyboard.KeyCode(char='b')}
# COMBINATION = {keyboard.Key.ctrl_l, keyboard.KeyCode(char='b')}

# # The currently active modifiers
# current = set()


# def on_press(key):
#     if key in COMBINATION:
#         current.add(key)
#         if all(k in current for k in COMBINATION):
#             print('All modifiers active!')
#     if key == keyboard.Key.esc:
#         listener.stop()


# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass


# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()

# from pynput import keyboard
# import time
# # The currently active modifiers
# current = set()


# KeyComb_Quit = [
#     {keyboard.Key.ctrl, keyboard.KeyCode(char='q')},
#     {keyboard.Key.ctrl_l, keyboard.KeyCode(char='q')},
#     {keyboard.Key.ctrl_r, keyboard.KeyCode(char='q')}

# ]


# def on_press(key):
#     if any([key in comb for comb in KeyComb_Quit]):
#         current.add(key)
#         if any(all(k in current for k in comb) for comb in KeyComb_Quit):
#             print("pressed")


# def on_release(key):
#     try:
#         current.remove(key)
#     except KeyError:
#         pass


# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()


from pynput.keyboard import Key, KeyCode, Listener


def function_1():
    """ One of your functions to be executed by a combination """
    print('Executed function_1')


def function_2():
    """ Another one of your functions to be executed by a combination """
    print('Executed function_2')


# Create a mapping of keys to function (use frozenset as sets/lists are not hashable - so they can't be used as keys)
# Note the missing `()` after function_1 and function_2 as want to pass the function, not the return value of the function
combination_to_function = {
    frozenset([Key.shift, KeyCode(vk=65)]): function_1,  # shift + a
    frozenset([Key.shift, KeyCode(vk=66)]): function_2,  # shift + b
    frozenset([Key.alt_l, KeyCode(vk=71)]): function_2,  # left alt + g
    frozenset([Key.ctrl_l, KeyCode(vk=71)]): function_2,  # left alt + g
}


# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in combination_to_function:  # Loop through each combination
        # Check if all keys in the combination are pressed
        if is_combination_pressed(combination):
            # If so, execute the function
            combination_to_function[combination]()


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
