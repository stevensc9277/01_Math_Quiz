#Import tkinter library
from tkinter import *

#Create an instance of Tkinter frame or window
win = Tk()

#Set the geometry of tkinter frame
win.geometry("750x250")
def callback():
   Label(win, text="Hello World!", font=('Georgia 20 bold')).pack(pady=4)

#Create a Label and a Button widget
btn = Button(win, text="Press Enter to Show a Message", command= callback)
btn.pack(ipadx=10)

win.bind('<Return>',lambda event:callback())

win.mainloop()