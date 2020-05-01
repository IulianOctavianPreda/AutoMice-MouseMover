from pynput import keyboard, mouse

import time
import threading
from random import seed
from random import random
from enum import Enum


class Pattern(Enum):
    Vertical = 1
    Horizontal = 2
    Random = 3

# TODO add timer for mouse movement, if the mouse was moved in the last x seconds do not trigger the automovement, or stop it if it was started
# TODO if the pressed key is ctrl, shift, alt add all 3 versions of it to the list


class UserInput():
    mouseController = mouse.Controller()

    keyCombination = {keyboard.Key.ctrl_l, keyboard.KeyCode(vk=65)}
    currentlyPressedKeys = set()
    threadFlag = threading.Event()

    distance = 10
    sleepTime = 1
    duration = 0.2
    patternSelected = Pattern.Horizontal

    def __init__(self):
        seed(time.time)
        threading.Thread(target=self.moveMouseAction, args=[]).start()
        with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease, args=[]) as listener:
            listener.join()

    def onPress(self, key):
        self.addKey(self.get_vk(key))
        if(self.isMatchingCombination()):
            if(self.threadFlag.is_set()):
                print("off")
                self.threadFlag.clear()
            else:
                print("on")
                self.threadFlag.set()

    def onRelease(self, key):
        self.removeKey(self.get_vk(key))

    def get_vk(self, key):
        return key.vk if hasattr(key, 'vk') else key.value.vk

    def addKey(self, keyPressed):
        self.currentlyPressedKeys.add(keyPressed)

    def removeKey(self, keyPressed):
        self.currentlyPressedKeys.remove(keyPressed)

    def isMatchingCombination(self):
        return all(self.get_vk(k) in self.currentlyPressedKeys for k in self.keyCombination)

    def moveMouseAction(self):
        print("thread")
        hasMoved = False
        while self.threadFlag.is_set():
            print("thread start")
            self.patternMatcher(hasMoved)
            time.sleep(self.sleepTime)

    def patternMatcher(self, hasMoved):
        if(self.patternSelected is Pattern.Horizontal):
            self.horizontalPattern(hasMoved)
        elif(self.patternSelected is Pattern.Vertical):
            self.verticalPattern(hasMoved)
        else:
            self.randomPattern()
        hasMoved = not hasMoved

    def verticalPattern(self, hasMoved):
        if(hasMoved):
            self.moveMouse(0, self.distance, self.duration)
        else:
            self.moveMouse(0, -(self.distance), self.duration)

    def horizontalPattern(self, hasMoved):
        if(hasMoved):
            self.moveMouse(self.distance, 0, self.duration)
        else:
            self.moveMouse(-(self.distance), 0, self.duration)

    def randomPattern(self):
        # Without detecting screen size the random number will be generated based on an average of 2 Full Hd screens
        screenHeight = 1080
        screenWidth = 1920
        x = random.randInt(0, screenWidth * 2)
        y = random.randInt(0, screenHeight)
        self.moveMouse(x, y, self.duration)

    def moveMouse(self, x, y, duration=0.2):
        sleepBetweenSteps = 0.05
        stepsNumber = int(duration/sleepBetweenSteps)
        stepX = int(x/stepsNumber)
        stepY = int(y/stepsNumber)
        startX, startY = self.mouseController.position

        for step in range(stepsNumber):
            self.mouseController.move(stepX, stepY)
            currentX, currentY = self.mouseController.position
            if(currentX == startX or currentX == startY):
                return
            time.sleep(sleepBetweenSteps)


controller = UserInput()
