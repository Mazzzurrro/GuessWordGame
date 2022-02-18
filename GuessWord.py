import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.app import App
from random import choice

Builder.load_file('GuessWord.kv')

class GuessWord(Widget):
    words=["words","crown","ideal"]
    word=choice(words)
    attempts=0
    def RandomWord(self):
        self.attempts=0        
        self.word=choice(self.words)
        l1=self.ids['OUTPUT']
        l1.text=""
        t1=self.ids['t1']
        t2=self.ids['t2']
        t3=self.ids['t3']
        t4=self.ids['t4']
        t5=self.ids['t5']
        listofletters=[t1,t2,t3,t4,t5]
        for i in range(5):
            listofletters[i].background_color=(1,1,1,1)
            listofletters[i].text=""
    def Check(self):
        self.attempts+=1
        t1=self.ids['t1']
        t2=self.ids['t2']
        t3=self.ids['t3']
        t4=self.ids['t4']
        t5=self.ids['t5']
        listofletters=[t1,t2,t3,t4,t5]
        outputstring=""
        accurateletters=0
        for i in range(5):
            listofletters[i].background_color=(1,1,1,1)
        for i in range(len(listofletters)):
            if listofletters[i].text.lower()=="":
                outputstring+=f'You have not filled {i+1} letter\n'                
            elif listofletters[i].text.lower() in self.word:
                if listofletters[i].text.lower() == self.word[i]:
                    listofletters[i].background_color=(0, 255/256, 0, 1)
                    accurateletters+=1
                    outputstring+=f'{listofletters[i].text.upper()} - letter in accurate spot\n'
                else:
                    listofletters[i].background_color=(228/256, 245/256, 39/256, 1)
                    outputstring+=f'{listofletters[i].text.upper()} - letter is in word, but not in this spot\n'
            else:
                outputstring+=f'{listofletters[i].text.upper()} - no letter in the word\n'
                listofletters[i].bacground_color=(1,1,1,1)
        l1=self.ids['OUTPUT']
        if accurateletters==5:
            l1.text=f'You have won! You guessed the word after {self.attempts} attempts'
        else:
            l1.text=outputstring
        
        
        


class GuessWord(App):
    def build(self):
        return GuessWord()

if __name__ == '__main__':
    GuessWord().run()