# needs to have a change-able shortcut
# input number of pixels to move, and the period, and how fast
# patterns
# start-up?
# from pynput.keyboard import Key, KeyCode, Controller, Listener
from pynput import keyboard, mouse

import pyautogui as pg
import time
import threading
from random import seed
from random import random
from enum import Enum


class Pattern(Enum):
    Vertical = 1
    Horizontal = 2
    Random = 3


class UserInput():
    pg.FAILSAFE = False

    keyCombination = {keyboard.Key.ctrl, keyboard.KeyCode(char='m')}
    currentlyPressedKeys = []
    isOn = False

    distance = 10
    sleepTime = 1
    duration = 0.2
    patternSelected = Pattern.Horizontal

    def __init__(self):
        seed(time.time)
        threading.Thread(target=self.moveMouseAction, args=[]).start()
        with keyboard.Listener(on_press=onPress, on_release=onRelease, args=[]) as listener:
            listener.join()

    def onPress(self, key):
        self.addKey(key)
        if(self.isMatchingCombination()):
            if(self.isOn):
                self.isOn = False
            else:
                self.isOn = True

    def onRelease(self, key):
        self.removeKey(key)

    def addKey(self, keyPressed):
        if keyPressed in self.keyCombination:
            self.currentlyPressedKeys.add(keyPressed)

    def removeKey(self, keyPressed):
        if keyPressed in self.keyCombination:
            self.currentlyPressedKeys.remove(keyPressed)

    def isMatchingCombination(self):
        if all(k in self.currentlyPressedKeys for k in self.keyCombination):
            return True
        else:
            return False

    def moveMouseAction(self):
        hasMoved = False
        while self.isOn:
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
            pg.moveRel(0, self.distance, duration=self.duration)
        else:
            pg.moveRel(0, -(self.distance), duration=self.duration)

    def horizontalPattern(self, hasMoved):
        if(hasMoved):
            pg.moveRel(self.distance, 0, duration=self.duration)
        else:
            pg.moveRel(-(self.distance), 0, duration=self.duration)

    def randomPattern(self):
        pg.sc
        pg.moveRel(self.distance, 0, duration=self.duration)
