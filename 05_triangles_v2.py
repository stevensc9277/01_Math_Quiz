import turtle
import math
from tkinter import *
import random

class Draw:
    def __init__(self, master):
        self.master = master
        self.master.title("Raw Turtle")
        self.canvas = Canvas(master)
        self.canvas.config(width=500, height=300)
        self.canvas.pack()
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("cyan")
        self.to_draw = turtle.RawTurtle(self.canvas)
        self.place_text = turtle.RawTurtle(self.canvas)

        # lists for angles and sides
        some_angles = []
        some_sides = []

        # generate angles and append to list
        a = random.randint(30, 90)
        b = random.randint(30, 89)
        some_angles.append(a)
        some_angles.append(b)

        # generate sides and append to list
        A = random.randint(5, 10)
        some_sides.append(A)

        self.finder(some_angles, some_sides)


    def triangle(self, displacement, angle):
        # initialise turtles
        self.to_draw.hideturtle()
        self.place_text.hideturtle()
        self.place_text.penup()

        self.to_draw.color("black")
        self.to_draw.pensize(5)
        self.place_text.write('A', font = 'style', move = True, align = 'right')
        self.to_draw.forward(displacement[0] * 10)  # Make to_draw draw a triangle
        self.to_draw.left(180 - angle[0])

        self.place_text.forward(displacement[0] * 10)  # move text
        self.place_text.write('B', font = 'style', align = 'left', move=True)	
        self.place_text.left(180 - angle[0])
        

        
        self.to_draw.forward(displacement[1] * 10)	
        self.to_draw.left(180 - angle[1])	
        
        self.place_text.forward(displacement[1] * 10)  # move text
        self.place_text.write('C', move = True, font = 'style', align = 'center')	
        self.to_draw.forward(displacement[2] * 10)
        # Complete the triangle
   


    def finder(self, angles, lengths):
        # print known angles for testing purposes
        print(angles[1], angles[0], lengths[0])

        # first find missing angle
        c = 180 - sum(angles)
        angles.append(c)

        # sort angles in ascending order
        angles.sort()

        # assume known side is smallest side
        B = (lengths[0] * math.sin(math.radians(angles[1]))) / math.sin(math.radians(angles[0]))
        C = (lengths[0] * math.sin(math.radians(angles[2]))) / math.sin(math.radians(angles[0]))
        print(round(B, 2), round(C, 2))
        lengths.append(round(B, 2))
        lengths.append(round(C, 2))
        perimeter = sum(lengths)
        print(lengths, perimeter)

        # sort out lengths to match respective angles
        lengths[0] = lengths[1]
        lengths[1] = lengths[2]
        lengths[2] = perimeter - (lengths[0] + lengths[1])
        print(lengths)
        self.triangle(lengths, angles)

if __name__ == '__main__':
    root = Tk()
    app = Draw(root)
    root.mainloop()