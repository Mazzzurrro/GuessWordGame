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
from kivy.clock import Clock
from random import choice
import math
from kivy.properties import StringProperty
import string 
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
import mysql.connector as sql
import numpy as np
import ast

mydb=sql.connect(user='root',password='mm1903',host='127.0.0.1',database='accounts_pythongame',auth_plugin='mysql_native_password')
#cursor = mydb.cursor()    
#cursor.execute(query)

letters= string.ascii_lowercase

def set_color(letter, color):
    COLORS_DICT  = {"W" : "ffffff", "Y" : "ffff00", "G" : "00ff00"}
    c = COLORS_DICT.get(color, "W")
    return f"[color={c}]{letter}[/color]"

class ScreenManager(ScreenManager):
    pass
class LoginScreen(Screen):
    pass
class RegisterScreen(Screen):
    pass

    
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
    def insert_text(self, substring, from_undo=False):
        pass
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print(keycode,text)
        focusedid = int(MyTextInput.focused[2])


        if keycode[1] == "backspace":
            if self.text=="":
                if int(MyTextInput.focused[2]) > 1:
                    self.text = ""
                    focusedid -= 1
                    MyTextInput.focused = "id" + str(focusedid)
            else:
                self.text = self.text[:-1]
        if keycode[1] == "right":
            if int(MyTextInput.focused[2]) < 5:
                focusedid += 1
                MyTextInput.focused = "id" + str(focusedid)
            elif int(MyTextInput.focused[2]) == 5:
                MyTextInput.focused = "id" + str(1)
                
        elif keycode[1] == "left":
            if int(MyTextInput.focused[2]) > 1:
                focusedid -= 1
                MyTextInput.focused = "id" + str(focusedid)
            elif int(MyTextInput.focused[2]) == 1:
                MyTextInput.focused = "id" + str(5)
        
        elif keycode[1] in letters:
            if int(MyTextInput.focused[2]) <= 5:
                self.text=text.upper()
                if int(MyTextInput.focused[2]) <5 :               
                    focusedid += 1
                    MyTextInput.focused = "id" + str(focusedid)
                
            
        self.change_focus()
        print("After changing", MyTextInput.focused)
        return True
    
    

        #TextInput.keyboard_on_key_down(self, window, keycode, text, modifiers)            

class MainScreen(Screen):
    myFile= open( "listofwords.txt", "r" )
    myLines = list( myFile )
    myFile.close()
    words = [line.rstrip('\n') for line in myLines]   
    wordsentrophy=words.copy()
    word=choice(words)
    listofguesses=[]
    accuratecolor=[]
    accurateletters=0
    answer=""
    with open('listofentrophies.txt') as f:      
        entrophyvalues = [ast.literal_eval(line) for line in f]
    print(entrophyvalues)
    
    newline='\n'
    entrophyval=""
    welcometext=StringProperty('Guess the word!')
    expectedinformations=[]
    expectedinformation=0
    attemptcount=0
    uncertaintynumber=math.log(len(words))/math.log(2)
    uncertainty=f'Possibilities:{len(words)}{newline}Uncertainty:{math.log(len(words))/math.log(2)}\n'
    wordcount=StringProperty(uncertainty)
    actualinformations=[]
    for i in range(5):
        entrophyval+=f'{i+1}: {entrophyvalues[i][0]} - {round(entrophyvalues[i][1],3)}{newline}'
    entrophyvaluesbest=StringProperty(entrophyval)
    listofoptions=[]
    entrophies={}
    possibleoptions={"G","W","Y"}
    for t1 in possibleoptions:
        for t2 in possibleoptions:
            for t3 in possibleoptions:
                for t4 in possibleoptions:
                    for t5 in possibleoptions:
                        possibility=[t1,t2,t3,t4,t5]
                        listofoptions.append(possibility)
    #for i in range(len(listofoptions)):
        #print(i+1,listofoptions[i])
    listofoptionsstring=[]
    for i in range(len(listofoptions)):
        string=""
        for j in range(5):
            string+=listofoptions[i][j]
        listofoptionsstring.append(string)

    dictionaryofoptions= {i : 0 for i in listofoptionsstring}
    
    def SetDict(self,string):
        dictletters={letter: 0 for letter in letters }
        for i in range(len(string)):
            dictletters[string[i]]+=1
        return dictletters
    
        
    def ClearLetters(self):
        MyTextInput.focused="id1"
        t1=self.ids.layout.ids.id1
        t2=self.ids.layout.ids.id2
        t3=self.ids.layout.ids.id3
        t4=self.ids.layout.ids.id4
        t5=self.ids.layout.ids.id5
        listofletters=[t1,t2,t3,t4,t5]
        for letter in listofletters:
            letter.text=""
    
    
    def FocusFirst(self,dt):
        self.ids.layout.ids.id1.focus=True
        
        
    def FocusNext(self,dt):
        if int(MyTextInput.focused[2])<5:
            newid=int(MyTextInput.focused[2])+1
            MyTextInput.focused="id"+str(newid)        
            self.ids.layout.ids[MyTextInput.focused].focus=True
    
    def DoSomething(self,instance):
        if int(MyTextInput.focused[2])<=5:
            if self.ids.layout.ids[MyTextInput.focused].text=="":
                self.ids.layout.ids[MyTextInput.focused].text=instance.text
            else:
                pass
    def BackspaceBehaviour(self):
        focusedid=int(MyTextInput.focused[2])        
        if self.ids.layout.ids[MyTextInput.focused].text=="":
            if int(MyTextInput.focused[2]) > 1:
                focusedid -= 1
                MyTextInput.focused = "id" + str(focusedid)
        else: 
            self.ids.layout.ids[MyTextInput.focused].text = ""
    def Backspacefocus(self):
        self.ids.layout.ids[MyTextInput.focused].focus=True
    
    def SetButtonColor(self,dt):
        listofletters=[]
        if len(self.answer)!=5:
            pass
        else:
            for i in self.answer:
                listofletters.append(i)
            
            for i in range(len(listofletters)):
                print(self.ids[listofletters[i].upper()].background_color)
                if self.accuratecolor[i]=="W":
                    #if color is yellow or green, don't colour
                    if self.ids[listofletters[i].upper()].background_color==[0.152, 0.96, 0.22, 1] or self.ids[listofletters[i].upper()].background_color==[0.96, 0.95, 0.15, 1]:
                        print("Color was green or yellow")
                    else:
                        self.ids[listofletters[i].upper()].background_color=[1, 0.38, 0.28, 1]
                if self.accuratecolor[i]=="Y":
                    #if color is green, don't color
                    print("Checked yellow letter",listofletters[i])
                    if self.ids[listofletters[i].upper()].background_color==[0.152, 0.96, 0.22, 1]:
                        print("Button color was green")
                    else:
                        self.ids[listofletters[i].upper()].background_color=[0.96, 0.95, 0.15, 1]
                if self.accuratecolor[i]=="G":
                    self.ids[listofletters[i].upper()].background_color=[0.152, 0.96, 0.22, 1]


        
        
        
    def StartGame(self):
        letters= string.ascii_lowercase
        for i in range(len(letters)):
            self.ids[letters[i].upper()].background_color=(136/255, 147/255, 137/255, 1)
        MyTextInput.focused="id1"
        self.uncertaintynumber=math.log(len(self.words))/math.log(2)
        self.actualinformations=[]
        self.wordcount=f'Possibilities:{len(self.words)}{self.newline}Uncertainty:{math.log(len(self.words))/math.log(2)}\n'
        self.wordsentrophy=self.words.copy()
        self.entrophyvaluescopy=self.entrophyvalues
        self.word=choice(self.words)
        self.attemptcount=0
        self.accurateletter=0
        entrophyvaluesbest=""
        newline='\n'        
        for i in range(5):
            try:
                entrophyvaluesbest+=f'{i+1}: {self.entrophyvalues[i][0]} - {round(self.entrophyvalues[i][1],3)}{newline}'
            except IndexError:
                pass
        self.entrophyvaluesbest=entrophyvaluesbest
        l1=self.ids['OUTPUT']
        l1.text=""
        t1=self.ids.layout.ids.id1
        t2=self.ids.layout.ids.id2
        t3=self.ids.layout.ids.id3
        t4=self.ids.layout.ids.id4
        t5=self.ids.layout.ids.id5  
        listofletters=[t1,t2,t3,t4,t5]
        for i in range(5):
            listofletters[i].text=""
        self.ids.layout.ids.id1.focus=True
        self.listofguesses=[]
    
    def CheckWinLose(self):
        if self.attemptcount<6:
            if self.accurateletters==5:
                attempts="" 
                attempts+=f'You won! The answer was: {self.word}{self.newline}Number of attempts: {self.attemptcount}'
                l1=self.ids['OUTPUT']
                l1.text=attempts
        else:
            if self.accurateletters==5:
                attempts="" 
                attempts+=f'You won! The answer was: {self.word}{self.newline}Number of attempts: {self.attemptcount}'
                l1=self.ids['OUTPUT']
                l1.text=attempts
            else:
                attempts="" 
                attempts+=f'You lost! The answer was: {self.word}'
                l1=self.ids['OUTPUT']
                l1.text=attempts
        
    def ShowPreviousWord(self):
        t1=self.ids.layout.ids.id1
        t2=self.ids.layout.ids.id2
        t3=self.ids.layout.ids.id3
        t4=self.ids.layout.ids.id4
        t5=self.ids.layout.ids.id5
        listofletters=[t1,t2,t3,t4,t5]
        string=""
        for i in listofletters:
            string+=i.text.upper()
        if len(string)!=5:
            pass
        else:
            coloredstring = "".join((set_color(l, c) for l, c in zip(string, self.accuratecolor)))
            self.listofguesses.append(coloredstring)
            attempts=""           
            for i in range(len(self.listofguesses)):
                attempts+=f'{i+1}: {self.listofguesses[i]} Gained information: {round(self.actualinformations[i],3)}\n'           
            l1=self.ids['OUTPUT']
            l1.text=attempts
    
    def Check(self):        
        self.accurateletters=0
        MyTextInput.focused="id1"
        self.welcometext=""
        t1=self.ids.layout.ids.id1
        t2=self.ids.layout.ids.id2
        t3=self.ids.layout.ids.id3
        t4=self.ids.layout.ids.id4
        t5=self.ids.layout.ids.id5
        listofletters=[t1,t2,t3,t4,t5]
        #outputstring=""
        self.answer=""
        for i in listofletters:
            self.answer+=i.text.lower()
        if len(self.answer)!=5:
            popup = Popup(title='Error!',content=Label(text=f'Write a 5 letter word'),size_hint=(None, None), size=(200, 100))
            popup.open()
        else:
            self.attemptcount+=1
            accuratecolorstr=self.SetPattern(self.answer,self.word)
            accuratecolor=[]
            for i in accuratecolorstr:
                accuratecolor.append(i)     
            self.accuratecolor=accuratecolor
            for i in self.accuratecolor:
                if i=="G":
                    self.accurateletters+=1
            attempts=""  
            if self.accurateletters==5:
                attempts+=f'You won! The answer was: {self.answer.upper()}'           
                l1=self.ids['OUTPUT']
                l1.text=attempts
                
                
    
            #Put actual information
            actualcombination=""
            for i in accuratecolor:
                actualcombination+=i
            self.actualcombination=actualcombination
            
    
            self.wordsentrophy=self.DeleteNotPossiblePattern(self.answer,self.wordsentrophy,accuratecolorstr)
    
            uncertainty=math.log(len(self.wordsentrophy))/math.log(2)
           
            actualinformation=self.uncertaintynumber-uncertainty
            self.uncertaintynumber=uncertainty
            self.actualinformations.append(actualinformation) 
            self.wordcount=f'Possibilities:{len(self.wordsentrophy)}{self.newline}Uncertainty:{str(math.log(len(self.wordsentrophy))/math.log(2))}\n'
            self.entrophyvaluescopy=self.EntrophyCount(self.wordsentrophy)
            entrophyvaluesbest=""
            newline='\n'
            for i in range(5):
                try:
                    entrophyvaluesbest+=f'{i+1}: {self.entrophyvaluescopy[i][0]} - {round(self.entrophyvaluescopy[i][1],3)}{newline}'
                except IndexError:
                    pass
            self.entrophyvaluesbest=entrophyvaluesbest
            #else:
                #l1.text=outputstring
   
    
    
    #SET pattern between solution and guess word
    def SetPattern(self,string,solution):
        accuratecolor=["0","1","2","3","4"]
        letters=self.SetDict(solution)
        #print(f'Letters: {letters}')
        for i in range(len(solution)):
            if letters[string[i]]>0:
                if string[i]==solution[i]:
                    accuratecolor[i]="G"
                    letters[string[i]]-=1
        #print("G",accuratecolor)
        
        for j in range(len(solution)):
            if letters[string[j]]>0:
                if string[j] in solution and accuratecolor[j]!="G":
                    accuratecolor[j]="Y"
                    letters[string[j]]-=1
                    
        #print("Y",accuratecolor)            
        for k in range(len(solution)):
            if accuratecolor[k]!="G" and accuratecolor[k]!="Y":
                accuratecolor[k]="W"
        #print("W",accuratecolor)
        accuratecolorstr=""
        for l in range(len(solution)):
            accuratecolorstr+=accuratecolor[l]
        return accuratecolorstr
    
    def NumberofPatterns(self,pattern):
        self.dictionaryofoptions[pattern]=self.dictionaryofoptions[pattern]+1    
   

    def EntrophyCount(self,lista):
        entrophies={}
        #Compare patterns of j word to list of i-words
        for j in range(len(lista)):
            for i in lista:
                pattern=self.SetPattern(lista[j],i)
                #Add one pattern which occured
                self.NumberofPatterns(pattern)
            print(f'Finished {j+1}/{len(lista)} words')
            #Count probability of pattern
            entrophy=0
            for k in self.dictionaryofoptions:
                self.dictionaryofoptions[k]=self.dictionaryofoptions[k]/len(lista)
                if self.dictionaryofoptions[k]!=0:
                    prob=self.dictionaryofoptions[k]
                    log=-math.log(self.dictionaryofoptions[k],2)
                    entrophy+=prob*log
            entrophies[lista[j]]=entrophy
        
        sort_orders = sorted(entrophies.items(), key=lambda x: x[1], reverse=True)
        return sort_orders
    
    def DeleteNotPossiblePattern(self,guess,possibilities,pattern):
        p=possibilities.copy()
        for i in range(len(pattern)):               
            if pattern[i]=="G":
                for j in possibilities:
                    if guess[i]!=j[i]:
                        #print(f'In word {j} the letter on {i+1} position is not equal')
                        try:
                            #print("USUWAM: G")
                            p.remove(j)
                        except ValueError:
                            pass
            
            if pattern[i]=="W":
                #print("The option: W")
                for j in possibilities:
                    if guess[i]==j[i]:
                        #print(f'In word {j} there is letter {guess[i]}')
                        try:
                            p.remove(j)
                        except ValueError:
                            pass
            
            if pattern[i]=="Y":
                #print("The option: Y")
                for j in possibilities:
                    if guess[i] not in j:
                        #print(f'In word {j} there is no letter {guess[i]}')
                        try:
                            p.remove(j)
                        except ValueError:
                            pass
                    if guess[i]==j[i]:
                        #print(f'In word {j} the letter on {i+1} position is equal')
                        try:
                            p.remove(j)
                        except ValueError:
                            pass

        return p
    
Builder.load_file("GuessWord.kv")
                 
class TestingappApp(App):
    def build(self):
        return MainScreen()
    
TestingappApp().run()