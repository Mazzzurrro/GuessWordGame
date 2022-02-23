import kivy
import sys
kivy.require('1.11.1')
sys.path.append("c:\\users\\dom\\appdata\\local\\programs\\python\\python39\\lib\\site-packages")
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from random import choice
Builder.load_file('GuessWord.kv')

def set_color(letter, color):
    COLORS_DICT  = {"W" : "ffffff", "Y" : "ffff00", "G" : "00ff00"}
    c = COLORS_DICT.get(color, "W")
    return f"[color={c}]{letter}[/color]"
    
class GuessWord(Widget):
    
    """
    def _on_keyboard(instance, key, scancode, codepoint, modifiers):
        if key==8:
            print("AJ")
        else:
            print("Keyboard pressed! {}".format(key))
    Window.bind(on_keyboard=_on_keyboard)
    """
    
    words=["words","crown","ideal"]
    word=choice(words)
    listofguesses=[]
    accuratecolor=[]
    accurateletters=0
    
    

    def ClearLetters(self):
        t1=self.ids['t1']
        t2=self.ids['t2']
        t3=self.ids['t3']
        t4=self.ids['t4']
        t5=self.ids['t5']
        word=self.ids['word']
        listofletters=[t1,t2,t3,t4,t5]
        for letter in listofletters:
            letter.text=""
        
    def StartGame(self):       
        self.word=choice(self.words)
        l1=self.ids['OUTPUT']
        l1.text=""
        listofletters=[]
        for i in range(5):
            name="t"+str(i)
            letter=self.ids[name]
            listofletters.append(name)
              
        for i in range(5):
            listofletters[i].background_color=(1,1,1,1)
            listofletters[i].text=""
        self.listofguesses=[]
    
    def ShowPreviousWord(self):
        t1=self.ids['t1']
        t2=self.ids['t2']
        t3=self.ids['t3']
        t4=self.ids['t4']
        t5=self.ids['t5']
        listofletters=[t1,t2,t3,t4,t5]
        string=""
        for i in listofletters:
            string+=i.text.upper()
        if string=="":
            pass
        else:
            coloredstring = "".join((set_color(l, c) for l, c in zip(string, self.accuratecolor)))
            self.listofguesses.append(coloredstring)
            attempts=""
            for i in range(len(self.listofguesses)):
                attempts+=f'Attempt {i+1}: {self.listofguesses[i]}\n'           
            l1=self.ids['OUTPUT']
            l1.text=attempts
        
    def Win(self):
        l1=self.ids['OUTPUT']
        l1.text+='You have won!'
        
    def Check(self):
        t1=self.ids['t1']
        t2=self.ids['t2']
        t3=self.ids['t3']
        t4=self.ids['t4']
        t5=self.ids['t5']
        listofletters=[t1,t2,t3,t4,t5]
        #outputstring=""
        accurateletters=0
        accuratecolor=[]
        
        for i in range(5):
            listofletters[i].background_color=(1,1,1,1)
        for i in range(len(listofletters)):
            if listofletters[i].text.lower()=="":
                #outputstring+=f'You have not filled {i+1} letter\n'
                accuratecolor.append("W")
            elif listofletters[i].text.lower() in self.word:
                if listofletters[i].text.lower() == self.word[i]:
                    accuratecolor.append("G")
                    #listofletters[i].background_color=(0, 255/256, 0, 1)
                    accurateletters+=1
                    #outputstring+=f'{listofletters[i].text.upper()} - letter in accurate spot\n'
                else:
                    accuratecolor.append("Y")
                    #listofletters[i].background_color=(228/256, 245/256, 39/256, 1)
                    #outputstring+=f'{listofletters[i].text.upper()} - letter is in word, but not in this spot\n'
            else:
                accuratecolor.append("W")
                #outputstring+=f'{listofletters[i].text.upper()} - no letter in the word\n'
                #listofletters[i].bacground_color=(1,1,1,1)
        self.accurateletters=accurateletters
        
        self.accuratecolor=accuratecolor       
        #else:
            #l1.text=outputstring
        
        
        


class GuessWordApp(App):
    def build(self):
        return GuessWord()

if __name__ == '__main__':
    GuessWordApp().run()