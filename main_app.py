from instructions import txt_instruction, txt_test1, txt_sits, txt_test2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from ruffier import test
from seconds import Seconds # Label
import csv
import os
from datetime import datetime

name = ""
age = 7
result1 = 0
result2 = 0
result3 = 0

      
def verify_int(str_num):
   try:
       return int(str_num)
   except Exception as e:
       print("Error:", e)
       return False
def save_to_csv(name, age, result1, result2, result3, evaluation): # save
    #time=datetime.now()
    filename = "results.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file,int)

        if not file_exists:# ko check key,chỉ file
            print("apper here")
            writer.writerow(["Name", "Age", "Pulse1", "Pulse2", "Pulse3", "Evaluation"])
        
        print("check")
        writer.writerow([name, age, result1, result2, result3, evaluation])
class MainWin(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)

       layout_main = BoxLayout(orientation="vertical")
       lb_intro = Label(font_size="25sp",text=" Ruffier")
       btn_start = Button(text="Start", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5})
       btn_start.on_press = self.next
       img_path = '123.png'
       if os.path.exists(img_path):
            img = Image(
                source=img_path,
                size_hint=(1, 0.6),
                allow_stretch=True,
                keep_ratio=True
            )
            layout_main.add_widget(img)
       else:
            print(f"Error: Image file not found at {img_path}")

       layout_main.add_widget(lb_intro)
       layout_main.add_widget(btn_start)

       self.add_widget(layout_main)

   def next(self):
       self.manager.current = "instruction"
class InstructionScr(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)

       lb_instr = Label(text=txt_instruction)
       lb_name = Label(text="Enter your name:")#name
       self.ip_name = TextInput(multiline=False)
       lb_age = Label(text="Enter your age:")#age
       self.ip_age = TextInput(multiline=False)
       btn_start = Button(text="Start", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5})
       btn_start.on_press = self.next

       layout_line1 = BoxLayout(height="30sp", size_hint=(0.8, None))
       layout_line1.add_widget(lb_name)
       layout_line1.add_widget(self.ip_name)

       layout_line2 = BoxLayout(height="30sp", size_hint=(0.8, None))
       layout_line2.add_widget(lb_age)
       layout_line2.add_widget(self.ip_age)

       layout_main = BoxLayout(orientation="vertical")
       layout_main.add_widget(lb_instr)
       layout_main.add_widget(layout_line1)
       layout_main.add_widget(layout_line2)
       layout_main.add_widget(btn_start)

       self.add_widget(layout_main)

   def next(self):
       global name, age
       name = self.ip_name.text
       age = verify_int(self.ip_age.text)
       if not age or age < 7:
           age = 7
           self.ip_age.text = str(age)
       self.manager.current = "pulse1"
class Pulse1Scr(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.next_screen = False

       lb_instr = Label(text=txt_test1)

       self.lb_seconds = Seconds(0)
       self.lb_seconds.bind(done=self.seconds_finished)

       lb_result = Label(text="Enter the result:", halign="right")
       self.ip_result = TextInput(text="0", multiline=False)
       self.ip_result.set_disabled(True)
       self.btn_next = Button(
           text="Start Timer", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
       )
       self.btn_next.on_press = self.next

       layout_line1 = BoxLayout(size_hint=(0.8, None), height="30sp")
       layout_line1.add_widget(lb_result)
       layout_line1.add_widget(self.ip_result)

       layout_main = BoxLayout(orientation="vertical", padding=8, spacing=8)
       layout_main.add_widget(lb_instr)
       layout_main.add_widget(self.lb_seconds)
       layout_main.add_widget(layout_line1)
       layout_main.add_widget(self.btn_next)
       self.add_widget(layout_main)

   def seconds_finished(self, *args):
       self.next_screen = True
       self.ip_result.set_disabled(False)
       self.btn_next.set_disabled(False)
       self.btn_next.text = "Next"

   def next(self):
       if not self.next_screen:
           self.btn_next.set_disabled(True)
           self.lb_seconds.start()
       else:
           global result1
           result1 = verify_int(self.ip_result.text)
           if not result1 or result1 < 0:
               result1 = 0
               self.ip_result.text = str(result1)
           self.manager.current = "sits"

class DoSquat(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)

       lb_instr = Label(text=txt_sits)
       self.btn_next = Button(
           text="Next", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
       )
       self.btn_next.on_press = self.next

       layout_main = BoxLayout(orientation="vertical", padding=8, spacing=8)
       layout_main.add_widget(lb_instr)
       layout_main.add_widget(self.btn_next)
       self.add_widget(layout_main)

   def next(self):
       self.manager.current = "pulse2"

class Pulse2Scr(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_screen1 = False
        self.lb_phase= Label(text="count your pulse")
        self.stage=0



        lb_instr = Label(text=txt_test2)
        lb_result1 = Label(text="Result:")
        self.ip_result1 = TextInput(multiline=False)
        lb_result2 = Label(text="Result after rest:")
        self.ip_result2 = TextInput(multiline=False)
        self.btn_start = Button(text="Start", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5})
        
        self.lb_seconds = Seconds(2)
        self.lb_seconds.bind(done=self.seconds_finished)
        self.ip_result1.set_disabled(True)
        
        self.ip_result2.set_disabled(True)
        self.btn_start.set_disabled(True)
        self.btn_start = Button(
            text="Start Timer", size_hint=(0.3, 0.2), pos_hint={"center_x": 0.5}
        )
        self.btn_start.on_press = self.next

        layout_line1 = BoxLayout(height="30sp", size_hint=(0.8, None))
        layout_line1.add_widget(lb_result1)
        layout_line1.add_widget(self.ip_result1)
        
        layout_line3 = BoxLayout(height="30sp", size_hint=(0.8, None))
        layout_line3.add_widget(self.lb_seconds)

        layout_line2 = BoxLayout(height="30sp", size_hint=(0.8, None))
        layout_line2.add_widget(lb_result2)
        layout_line2.add_widget(self.ip_result2)


        layout_main = BoxLayout(orientation="vertical")
        layout_main.add_widget(lb_instr)
        layout_main.add_widget(self.lb_phase)
        layout_main.add_widget(layout_line3)
        layout_main.add_widget(layout_line1)
        layout_main.add_widget(layout_line2)
        layout_main.add_widget(self.btn_start)

        self.add_widget(layout_main)
    def seconds_finished(self, *args):

        if self.lb_seconds.done:
            if self.stage==0:
                self.ip_result1.set_disabled(False)
                self.lb_seconds.restart(2)
                self.stage=1
                self.lb_phase.text="rest"
            elif self.stage == 1:
                self.lb_seconds.restart(2)
                self.stage=2
                self.lb_phase.text="hold your pulse"
            elif self.stage==2:
                    self.ip_result2.set_disabled(False)    
                    self.next_screen1 = True
                    self.btn_start.set_disabled(False)
                    self.btn_start.text = "Next"

    def next(self):
        if not self.next_screen1:
            self.btn_start.set_disabled(True)
            self.lb_seconds.start()

        else:
            global result2, result3
            result2 = verify_int(self.ip_result1.text)
            result3 = verify_int(self.ip_result2.text)

            if not result2 or result2 < 0:
                result2 = 0
                self.ip_result1.text = str(result2)
            elif not result3 or result3 < 0:
                result3 = 0
                self.ip_result2.text = str(result3)
            else:
                self.manager.current = "result"

class ResultScr(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)

       self.lb_instr = Label(text="")

       layout_main = BoxLayout(orientation="vertical")
       layout_main.add_widget(self.lb_instr)
       self.add_widget(layout_main)

       self.on_enter = self.before

   def before(self):
        global name, age, result1, result2, result3

        evaluation = test(result1, result2, result3, age)

        self.lb_instr.text = name + "\n" + evaluation

        
        #save_to_csv(name, age, result1, result2, result3, evaluation)
        save_to_csv("minh", 19, 180, 182, 183, 195)




class MyApp(App):
   def build(self):
       sm = ScreenManager()
       Window.clearcolor = (0.6, 0.6, 0.8, 1)
       sm.add_widget(MainWin(name="introdution"))
       sm.add_widget(InstructionScr(name="instruction"))
       sm.add_widget(Pulse1Scr(name="pulse1"))
       sm.add_widget(DoSquat(name="sits"))
       sm.add_widget(Pulse2Scr(name="pulse2"))
       sm.add_widget(ResultScr(name="result"))
       return sm


app = MyApp()
app.run()


