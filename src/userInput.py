from pynput import keyboard, mouse
from enums.patterns import Pattern
from enums.keysMapping import KeysMapping
import time
import threading
import random
import timeit
import copy
import os


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
        self.updateFromUserSettingsFile()

    def addListeners(self):
        keyboard.Listener(on_press=self.onPress,
                          on_release=self.onRelease, args=[]).start()
        mouse.Listener(on_move=self.onMove, on_click=self.onClick,
                       on_scroll=self.onScroll, args=[]).start()

    def addListenersBlocking(self):
        with keyboard.Listener(on_press=self.onPress, on_release=self.onRelease, args=[]) as keyboardListener, mouse.Listener(on_move=self.onMove, on_click=self.onClick, on_scroll=self.onScroll, args=[]) as mouseListener:
            keyboardListener.join()
            mouseListener.join()

    def onMove(self, x, y):
        self.resetTimer()

    def onScroll(self, x, y, dx, dy):
        self.resetTimer()

    def onClick(self, x, y, button, pressed):
        self.resetTimer()

    def resetTimer(self):
        self.timer = time.time()

    def onPress(self, key):
        self.timer = time.time()
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
        x = random.randint(-(self.distance), self.distance)
        y = random.randint(-(self.distance), self.distance)
        self.moveMouse(x, y, self.duration)

    def moveMouse(self, x, y, duration=0.2):
        sleepBetweenSteps = 0.05
        stepsNumber = int(duration/sleepBetweenSteps)
        maxSteps = self.max(x, y)
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

    def updateUserSettingsFile(self):
        f = open("MouseMoverSettings", "w+")
        keyCombo = ','.join(str(s) for s in self.keyCombination)
        data = f'distance={self.distance}\nwaitTime={self.waitTime}\nduration={self.duration}\npatternSelected={self.patternSelected.name}\nkeyCombination={keyCombo}'
        f.write(data)
        f.close()

    def updateFromUserSettingsFile(self):
        if os.path.isfile('MouseMoverSettings') and os.stat('MouseMoverSettings').st_size != 0:
            f = open("MouseMoverSettings", "r")
            data = f.readlines()
            curatedData = [line.strip()
                           for line in data if line.strip() != "" and '=' in line]
            d = dict(x.split("=") for x in curatedData)
            f.close()

            if("distance" in d):
                try:
                    self.distance = int(d["distance"])
                except:
                    pass
            if("waitTime" in d):
                try:
                    self.waitTime = float(d["waitTime"])
                except:
                    pass
            if("duration" in d):
                try:
                    self.duration = float(d["duration"])
                except:
                    pass
            if("patternSelected" in d):
                try:
                    self.patternSelected = Pattern[d["patternSelected"]]
                except:
                    pass
            if("keyCombination" in d):
                keyValues = d["keyCombination"].split(',')
                s = set()
                for item in keyValues:
                    try:
                        s.add(int(item))
                    except:
                        pass
                self.keyCombination = copy.deepcopy(s)


if __name__ == "__main__":
    controller = UserInput()
    controller.addListenersBlocking()
    controller.updateUserSettingsFile()
