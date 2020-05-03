from pynput import keyboard, mouse
from enums.patterns import Pattern
from enums.keysMapping import KeysMapping
import time
import threading
import random
import timeit
import copy

# TODO save user defined specs


class UserInput():
    mouseController = mouse.Controller()
    timer = time.time()
    keyMapping = {x.name: x.value for x in KeysMapping}

    keyCombination = {KeysMapping.Left_Ctrl.value, 77}  # Ctrl_l + M

    currentlyPressedKeys = set()
    isOn = False
    isChangingKeyCombination = False

    sleepBetweenSteps = 0.05

    distance = 10
    waitTime = 5
    duration = 0.2
    patternSelected = Pattern.Horizontal

    @property
    def keyCombo(self):
        keys = sorted([self.getCharacter(x)
                       for x in self.keyCombination], key=len, reverse=True)
        return ' + '.join(keys)

    @property
    def inactiveTime(self):
        return time.time() - self.timer

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
        self.addKey(self.getVk(key))
        if(not self.isChangingKeyCombination):
            if(self.isMatchingCombination()):
                if(not self.isOn):
                    self.turnOn()
                else:
                    self.turnOff()
        else:
            self.keyCombination = copy.deepcopy(self.currentlyPressedKeys)

    def turnOn(self):
        if(not self.isOn):
            self.isOn = True
            threading.Thread(target=self.moveMouseAction, args=[]).start()

    def turnOff(self):
        self.isOn = False

    def onRelease(self, key):
        self.removeKey(self.getVk(key))

    def getVk(self, key):
        return key.vk if hasattr(key, 'vk') else key.value.vk

    def getCharacter(self, code):
        for name, value in self.keyMapping.items():
            if code == value:
                return self.snakeCaseToHuman(name)
        else:
            return chr(code)

    def snakeCaseToHuman(self, string):
        return string.replace('_', " ")

    def addKey(self, keyPressed):
        self.currentlyPressedKeys.add(keyPressed)

    def removeKey(self, keyPressed):
        self.currentlyPressedKeys.remove(keyPressed)

    def isMatchingCombination(self):
        return all(k in self.currentlyPressedKeys for k in self.keyCombination)

    def moveMouseAction(self):
        hasMoved = False
        while self.isOn:
            if(self.inactiveTime > self.waitTime):
                self.patternMatcher(hasMoved)
                hasMoved = not hasMoved
                time.sleep(self.waitTime)
            else:
                time.sleep(self.waitTime - self.inactiveTime)

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
        maxSteps = self.max(x, y)
        print(stepsNumber, duration, maxSteps, x, y)
        if(stepsNumber > maxSteps):
            stepsNumber = int(maxSteps)
        stepX = int(x/stepsNumber)
        stepY = int(y/stepsNumber)
        startX, startY = self.mouseController.position

        for step in range(stepsNumber):
            self.mouseController.move(stepX, stepY)
            currentX, currentY = self.mouseController.position
            if(currentX == startX or currentX == startY):
                return
            time.sleep(sleepBetweenSteps)

    def max(self, x, y):
        if abs(x) > abs(y):
            return abs(x)
        else:
            return abs(y)


if __name__ == "__main__":
    controller = UserInput()
    controller.addListenersBlocking()
