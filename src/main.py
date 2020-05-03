import PySimpleGUI as sg
from userInput import UserInput
from enums.patterns import Pattern
from ico import ico
import base64
import os

patterns = [{"key": "Pattern" + str(x.value), "value": x}
            for x in Pattern]
userInput = UserInput()
userInput.addListeners()
oldValues = None

tempIconFile = "ico.ico"


def createTempIco():
    icondata = base64.b64decode(ico)
    iconfile = open(tempIconFile, "wb")
    iconfile.write(icondata)
    iconfile.close()


def removeTempIco():
    os.remove(tempIconFile)


def updatePattern(value):
    for pattern in patterns:
        if(pattern["value"] == value):
            window[pattern["key"]].update(True)
        else:
            window[pattern["key"]].update(False)


def timeAsInt(time):
    return int(round(time * 100))


def updateValues(values):
    try:
        userInput.distance = int(values['Distance'])
    except:
        window['Distance'].update(userInput.distance)

    try:
        window['Duration'].update(userInput.duration)
    except:
        userInput.duration = float(values['Duration'])

    try:
        userInput.waitTime = float(values['WaitTime'])
    except:
        window['WaitTime'].update(userInput.waitTime)

    for pattern in patterns:
        if values[pattern["key"]]:
            userInput.patternSelected = pattern["value"]


sg.theme('DarkBlue')
layout = [
    [sg.Input(visible=False)],
    [sg.Text('Current key combination:', size=(20, 1)),
     sg.Text(size=(20, 1), key='KeyCombination'),
     sg.Button(button_color=("white", "black"),
               button_text='Change', key='ChangeCombination')
     ],
    [sg.Text('Distance in pixels to move:', size=(20, 1)),
     sg.Input(size=(15, 1), key='Distance')
     ],
    [sg.Text('Inactive seconds to wait:', size=(20, 1)),
     sg.Input(size=(15, 1), key='WaitTime')
     ],
    [sg.Text('Duration of the movement:', size=(20, 1)),
     sg.Input(size=(15, 1), key='Duration')
     ],

    [sg.Text('Movement pattern:')] + [sg.Radio(pattern.name, "radio_group1",
                                               key="Pattern" + str(pattern.value)) for pattern in Pattern],
    [sg.Text('Current inactive time:', size=(20, 1)),
     sg.Text(size=(20, 1), key='InactiveTime')
     ],
    [sg.Text(size=(20, 1)),
     sg.Text(size=(20, 1),),
     sg.Button(button_color=("white", "black"),
               button_text="Start",  key='StartStop')
     ]
]

createTempIco()
window = sg.Window('Mouse Mover', layout, icon=tempIconFile, finalize=True)
window.read(timeout=10)
window['KeyCombination'].update(userInput.keyCombo)
window['Distance'].update(userInput.distance)
window['WaitTime'].update(userInput.waitTime)
window['Duration'].update(userInput.duration)
updatePattern(userInput.patternSelected)


while True:  # Event Loop
    event, values = window.read(timeout=10)
    if event in (None, 'Exit'):
        userInput.turnOff()
        break

    if(userInput.isOn):
        window['StartStop'].update("Stop")
        window['InactiveTime'].update('{:02d}:{:02d}.{:02d}'.format((timeAsInt(userInput.inactiveTime) // 100) // 60,
                                                                    (timeAsInt(
                                                                        userInput.inactiveTime) // 100) % 60,
                                                                    timeAsInt(userInput.inactiveTime) % 100))
    else:
        window['StartStop'].update("Start")

    if(userInput.isChangingKeyCombination):
        window['KeyCombination'].update(userInput.keyCombo)

    if oldValues != values:
        updateValues(values)

    if event == 'ChangeCombination':
        if(userInput.isChangingKeyCombination):
            userInput.isChangingKeyCombination = False
            window['ChangeCombination'].update("Change")
        else:
            userInput.isChangingKeyCombination = True
            window['ChangeCombination'].update("Finish")

    if event == 'StartStop':
        if(userInput.isOn):
            userInput.turnOff()
        else:
            userInput.turnOn()


window.close()
removeTempIco()
