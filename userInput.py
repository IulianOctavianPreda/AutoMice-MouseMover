from pynput import keyboard, mouse
from enums.patterns import Pattern
import time
import threading
import random
import timeit


class UserInput():
    mouseController = mouse.Controller()
    timer = time.time()

    keyCombination = {keyboard.Key.ctrl_l, keyboard.KeyCode(vk=65)}
    currentlyPressedKeys = set()
    isOn = False

    distance = 10
    waitTime = 5
    duration = 0.2
    patternSelected = Pattern.Horizontal

    def __init__(self):
        random.seed(time.time)

    def addListeners(self):
        keyboard.Listener(on_press=self.onPress,
                          on_release=self.onRelease, args=[]).start()
        mouse.Listener(on_move=self.onMove, args=[]).start()

    def addListenersBlocking(self):
        with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease, args=[]) as keyboardListener, mouse.Listener(on_move=self.onMove, args=[]) as mouseListener:
            keyboardListener.join()
            mouseListener.join()

    def onMove(self, x, y):
        self.timer = time.time()

    def onPress(self, key):
        self.addKey(self.get_vk(key))
        if(self.isMatchingCombination()):
            if(not self.isOn):
                self.turnOn()
            else:
                self.turnOff()

    def turnOn(self):
        if(not self.isOn):
            self.isOn = True
            threading.Thread(target=self.moveMouseAction, args=[]).start()

    def turnOff(self):
        self.isOn = False

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
        hasMoved = False
        while self.isOn:
            elapsedTime = time.time() - self.timer
            if(elapsedTime > self.waitTime):
                self.patternMatcher(hasMoved)
                hasMoved = not hasMoved
                time.sleep(self.waitTime - 1)

    def patternMatcher(self, hasMoved):
        if(self.patternSelected is Pattern.Horizontal):
            self.horizontalPattern(hasMoved)
        elif(self.patternSelected is Pattern.Vertical):
            self.verticalPattern(hasMoved)
        else:
            self.randomPattern()

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
        # Without detecting screen size the random number will be generated in a window of 500x500 relative to the mouse position
        screenHeight = 500
        screenWidth = 500
        x = random.randint(-screenWidth, screenWidth)
        y = random.randint(-screenHeight, screenHeight)
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


if __name__ == "__main__":
    controller = UserInput()
    controller.addListenersBlocking()
