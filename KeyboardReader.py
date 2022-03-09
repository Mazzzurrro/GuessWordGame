from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

Builder.load_file("keyboardreader.kv")

class MyTextInput(TextInput):
    focused = 'id1'

    def change_focus(self, *args):
        app = App.get_running_app()
        if app.root is not None:
            # Now access the container.
            layout = app.root.ids["layout"]
            # Access the required widget and set its focus.
            print("Changefocus", MyTextInput.focused)
            layout.ids[MyTextInput.focused].focus = True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        focusedid = int(MyTextInput.focused[2])
        if keycode[1] == "backspace":
            self.text = self.text[:-1]
        if keycode[1] == "right":
            if int(MyTextInput.focused[2]) < 5:
                focusedid += 1
                MyTextInput.focused = "id" + str(focusedid)
        elif keycode[1] == "left":
            if int(MyTextInput.focused[2]) > 1:
                self.text = ""
                focusedid -= 1
                MyTextInput.focused = "id" + str(focusedid)
        self.change_focus()
        print("After changing", MyTextInput.focused)
        return True

        #TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)            

class MainScreen(Widget):
    pass
    
                 
class TestingappApp(App):
    def build(self):
        return MainScreen()
    
TestingappApp().run()