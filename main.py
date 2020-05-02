
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from functools import partial
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy import require

from userInput import UserInput

Builder.load_string('''
<ModeScreen>:
    distance: distance
    waitTime: waitTime
    pattern: pattern
    duration: duration
    FloatLayout:
        BoxLayout:
            size_hint: 0.8, 0.8
            pos_hint: {"x": 0.1, "y": 0.1}
            padding: "5sp"
            spacing: "5sp"
            Label:
                canvas:
                    Color:
                        rgba: 0, 0, 1, 0.3
                    Rectangle:
                        pos: self.pos
                        size: self.size
                text: "Mouse mover"
                size_hint_y: 0.1
            
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.1
                padding: "5sp"
                Widget:
                    size_hint_x: 0.2
                Label:
                    text: "Distance to move(in pixels):"
                TextInput:
                    id: distance
                    text: distance.text
                    on_text:root.inputDistance(self.text)
                Widget:
                    size_hint_x: 0.2

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.1
                padding: "5sp"
                Widget:
                    size_hint_x: 0.2
                Label:
                    text: "Move mouse whenever the computer remains idle for:"
                TextInput:
                    id: waitTime
                    on_text:root.inputWaitTime(self.text)
                Widget:
                    size_hint_x: 0.2
            
            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.1
                padding: "5sp"
                Widget:
                    size_hint_x: 0.2
                Label:
                    text: "Movement duration:"
                TextInput:
                    id: duration
                    on_text:root.inputDuration(self.text)
                Widget:
                    size_hint_x: 0.2

            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.1
                padding: "5sp"
                Widget:
                    size_hint_x: 0.2
                Label:
                    text: "Select movement pattern:"
                Spinner:
                    id: pattern
                    values: "Vertical","Horizontal","Random"
                    on_text:root.selectedPattern(self.text)
                Widget:
                    size_hint_x: 0.2

            Widget:
                size_hint_y: 0.1
            BoxLayout:
                orientation: "horizontal"
                size_hint: 0.5,0.1
                Button:
                    text: "Stop"
                    on_release: root.stop()
                Button:
                    text: "Start"
                    on_release: root.start()

''')


class ModeScreen(Screen):
    userInput = UserInput()
    userInput.addListeners()

    distance = ObjectProperty()
    waitTime = ObjectProperty()
    pattern = ObjectProperty()
    duration = ObjectProperty()

    distance.text = str(userInput.distance)

    def inputDistance(self, text):
        pass
    #     distance = int(text)
    #     if(distance > )
    #     self.userInput.distance

    def inputWaitTime(self, text):
        pass

    def inputDuration(self, text):
        pass

    def selectedPattern(self, text):
        pass

    def set_mode(self, mode):
        """ Sets the keyboard mode to the one specified """
        Config.set("kivy", "keyboard_mode", mode.replace("'", ""))
        Config.write()
        self.center_label.text = "Please restart the application for this\n" \
            "setting to take effect."

    def start(self):
        self.userInput.turnOn()

    def stop(self):
        self.userInput.turnOff()


class MouseMover(App):
    sm = None  # The root screen manager

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(ModeScreen(name="mode"))
        self.sm.current = "mode"
        return self.sm


if __name__ == "__main__":
    MouseMover().run()
