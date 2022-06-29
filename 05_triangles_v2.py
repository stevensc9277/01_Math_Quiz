import turtle
import math
from tkinter import *
import random

from numpy import angle

# lists for angles and sides
some_angles = []
some_sides = []

class Draw:
    def __init__(self, master):
        back = "light blue"
        self.master_frame = Frame(root, bg=back, width=500, height=275)
        self.master_frame.grid()
        self.master_frame.config(bg="light blue")
  
        self.canvas = Canvas(self.master_frame)

        self.canvas.grid(row=0)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(back)
        self.to_draw = turtle.RawTurtle(self.screen)
        self.place_text = turtle.RawTurtle(self.screen)
        self.questions_frame = Frame(self.master_frame, bg=back)
        self.questions_frame.grid(row=1)

        self.question_label = Label(self.questions_frame, bg=back, text="Find the area and perimeter of the above triangle", font="arial 10 bold")
        self.question_label.grid(row=0, padx=10, pady=10, sticky="NEWS")

        self.user_lengths_label = Label(self.questions_frame, bg=back, justify=CENTER, font="arial 10 italic")
        self.user_lengths_label.grid(row=1, padx=10)

        # make entry labels and labels with a new frame
        self.area_perimeter_frame = Frame(self.master_frame, bg=back)
        self.area_perimeter_frame.grid()
        self.area_label = Label(self.area_perimeter_frame, font="arial 13", text="Area", justify=LEFT, bg=back)
        self.area_label.grid(row=0, column=0, pady=10, padx=10, sticky="NEWS")
        self.area_entry = Entry(self.area_perimeter_frame, justify=CENTER, fg="grey")
        self.area_entry.insert(0, "A = 0.5 x b x h")

        # bind commands, shows formulae if no input is detected or does nothing
        self.area_entry.bind("<FocusIn>", lambda e: self.on_enter(e, self.area_entry))
        self.area_entry.bind("<FocusOut>", lambda e: self.on_leave(e, self.area_entry))
        self.area_entry.grid(row=0, column=1, ipady=12, pady=5)

        self.perimeter_label = Label(self.area_perimeter_frame, font="arial 13", text="Perimeter", justify=LEFT, bg=back)
        self.perimeter_label.grid(row=1, column=0, padx=10, pady=10, sticky="NEWS")
        self.perimeter_entry = Entry(self.area_perimeter_frame, justify=CENTER, fg="grey")
        self.perimeter_entry.insert(0, "P = AB + BC + CA")
        self.perimeter_entry.bind("<FocusIn>", lambda e: self.on_enter(e, self.perimeter_entry))
        self.perimeter_entry.bind("<FocusOut>", lambda e: self.on_leave(e, self.perimeter_entry))
        self.perimeter_entry.grid(row=1, column=1, padx=10, pady=10, ipady=12)

        # buttons to submit answers
        self.area_submit = Button(self.area_perimeter_frame, text="Submit", padx=10, pady=10, command= lambda: self.answer_check(self.area_entry, some_sides))
        self.area_submit.grid(row=0, column=2)

        self.perimeter_submit = Button(self.area_perimeter_frame, text="Submit", padx=10, pady=10, command= lambda: self.answer_check(self.perimeter_entry, some_sides))
        self.perimeter_submit.grid(row=1, column=2)

        self.do_this()
        

    def do_this(self):
        # generate angles and append to list
        a = random.randint(30, 80)
        b = 90 - a      # ensures triangle is always a right angle triangle
        some_angles.append(a)
        some_angles.append(b)

        # generate sides and append to list
        A = random.randint(10, 19)
        some_sides.append(A)

        self.finder(some_angles, some_sides)
       

    def on_enter(self, e, name):  # changes entry label fg back to black
        user_input = name.get()
        if user_input == "A = 0.5 x b x h" or user_input == "P = AB + BC + CA":
            name.delete(0, "end")
            name['foreground'] = 'black'
    
    def on_leave(self, e, name):  # changes entry label fg back to black and shows formulae if there was no input given
        user_input =  name.get()
        if name == self.area_entry and user_input == "":
            name.insert(0, "A = 0.5 x b x h")
        
        elif name == self.perimeter_entry and user_input == "":
            name.insert(0, "P = AB + BC + CA")

        if user_input == "":
            name['foreground'] = 'grey'
        
        else:
            name['foreground'] = 'black'
            name.unbind("<FocusOut>")
         
    # draw triangle
    def triangle(self, displacement, angle):
        self.user_lengths_label.config(text="AB: {}, BC: {}, CA: {}".format(displacement[0], displacement[1], displacement[2]))
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
        self.place_text.write('B', font = 'style', align = 'right', move=True)	
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
        angles.sort(reverse=True)
        print(angles)

        # assume known side is smallest side
        B = (lengths[0] * math.sin(math.radians(angles[1]))) / math.sin(math.radians(angles[0]))
        C = (lengths[0] * math.sin(math.radians(angles[2]))) / math.sin(math.radians(angles[0]))

        # round to 2dp and append lengths to list
        B = round(B, 2)
        C = round(C, 2)
        lengths.append(B)
        lengths.append(C)

        # find perimeter and area
        perimeter = sum(lengths)
        print(lengths, perimeter)

        # sort out lengths to match respective angles
        # lengths[0] = lengths[1]
        # lengths[1] = lengths[2]
        # lengths[2] = int(perimeter - lengths[0] - lengths[1])
        lengths.sort()
        print("First length is {} before sort, second length is {}".format(lengths[0], lengths[1]))
        lengths[0] = lengths[1]
        
        lengths[1] = round(perimeter - lengths[0] - lengths[2], 2)
        print("First length is {} after sort, second length is {}".format(lengths[0], lengths[1]))
        area = round(0.5*lengths[0] * lengths[1], 2)
        
        print(lengths, area)
        
        self.triangle(lengths, angles)
    
    def answer_check(self, name, lengths):
        # get user input
        try:
            answer = float(name.get())

            if name == self.area_entry:

                # calculate area, see if it matches user input
                area = round(0.5 * lengths[0] * lengths[1], 2)
                print("Area given is ", answer)
                print("Actual area is ", area)
                print()

                if answer != area:
                    self.area_entry.config(bg="#ffafaf")
                
                else:
                    self.area_entry.config(bg="#98FB98")
                    self.area_submit.config(state=DISABLED)
        
            else:
                perimeter = round(sum(lengths), 2)
                print("Perimeter given is ", answer)
                print("Actual perimeter is ", perimeter)
                print()

                if answer != perimeter:
                    self.perimeter_entry.config(bg="#ffafaf")
                
                else:
                    self.perimeter_entry.config(bg="#98FB98")
                    self.perimeter_submit.config(state=DISABLED)

            # if both area and perimeter answers are correct, generate a new question
            if self.perimeter_entry.cget("bg") == "#98FB98" and self.area_entry.cget("bg") == "#98FB98":
                print("Both are correct!")
                some_angles.clear()
                some_sides.clear()
                self.screen.resetscreen()
                self.perimeter_submit.config(state=NORMAL)
                self.area_submit.config(state=NORMAL)
                self.perimeter_entry.config(bg="white")
                self.area_entry.config(bg="white")
                self.do_this()                

            else:
                print("Something went wrong")

        except ValueError:
            name.delete(0, "end")
            name.config(bg="#ffafaf")
            name.insert(0, "Please enter a float")
            name.after(1500, lambda e: name.delete(0, "end"), name.config(bg="white"))

    

        

if __name__ == '__main__':
    root = Tk()
    root.title("Turtle Triangle")
    app = Draw(root)
    root.mainloop()