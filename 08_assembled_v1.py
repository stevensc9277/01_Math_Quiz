from tkinter import *
# randomly select operator (+, -, *, / )
import operator
from functools import partial
import random
import turtle
import math


# lists for angles and sides
some_angles = []
some_sides = []
score = 0
number = 1

class Start:
    def __init__(self, parent):
        
        
        back_ground = "light blue"
        # initialise start frame GUI
        self.start_frame = Frame(root, bg=back_ground)
        self.start_frame.grid()


        # create labels (Heading & instructions)
        self.start_label = Label(self.start_frame, bg=back_ground, text="Math Quiz", font="Arial 14 bold", justify=CENTER)
        self.start_label.grid(row=0, padx=10, pady=10)
        
        self.start_instructions = Label(self.start_frame, bg=back_ground, text="Please select a difficulty level to proceed to the quiz.", justify=CENTER, wrap=250)
        self.start_instructions.grid(row=1, padx=10, pady=10)

        # create button frame (row 2)
        self.button_frame = Frame(self.start_frame, bg=back_ground)
        self.button_frame.grid(row=2)

        # set up buttons in button frame, added padding
        self.easy_button = Button(self.button_frame, text="Easy", font="Arial 12 italic", bg="#90EE90", command=lambda: self.to_quiz(1))
        self.easy_button.grid(row=0, column=0, padx=10, pady=10)

        self.medium_button = Button(self.button_frame, text="Medium", font="Arial 12 italic", bg="#FFFFA1", command=lambda: self.to_quiz(2))
        self.medium_button.grid(row=0, column=1, padx=10, pady=10)

        self.hard_button = Button(self.button_frame, text="Hard", font="Arial 12 italic", bg="#FFCCCB", command=lambda: self.to_draw())
        self.hard_button.grid(row=0, column=2, padx=10, pady=10)

        # help button (row 3)
        self.help_button = Button(self.start_frame, text="Help", font="Arial 12", command=self.to_help)
        self.help_button.grid(row=3, padx=10, pady=10)

    def to_draw(self):
        do_draw = Draw(self)


    def to_help(self):
        # redirect to a separate frame to give more detailed information of the game to user
        get_help = Help(self)
        root.withdraw()
    
    def to_quiz(self, difficulty):
        # redirect to quiz
        show_quiz = Quiz(self, difficulty)
        root.withdraw()


class Quiz:
    def __init__(self, partner, difficulty):

        back_ground = "light blue"
        # Create quiz gui and set up grid
        self.quiz_box = Toplevel()
        
        self.quiz_frame = Frame(self.quiz_box, bg=back_ground)
        self.quiz_frame.grid()

        # if users press cross at top, quiz quits
        self.quiz_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        # heading row (row 0)
        self.quiz_heading = Label(self.quiz_frame, text="Math Quiz: ", justify=LEFT, font="arial 14 bold", bg=back_ground)
        self.quiz_heading.grid(row=0, padx=10, pady=10, sticky=W)

        self.quiz_score = Label(self.quiz_frame, text="Score: 0", font="arial 11 italic", bg=back_ground)
        self.quiz_score.grid(row=0, sticky=E)

        # Question label
        self.question_label = Label(self.quiz_frame, text="question goes here", font="arial 12 bold", justify=CENTER, bg=back_ground)
        self.question_label.grid(row=1, padx=10, pady=10)
        # Entry box, Button & Error label (row 2)
        self.entry_error_frame = Frame(self.quiz_frame, bg=back_ground)
        self.entry_error_frame.grid(row=2, padx=10, pady=10)

        self.answer_entry = Entry(self.entry_error_frame, font="Arial 19 bold", width=12, justify=CENTER)
        self.answer_entry.grid(row=0, column=0)
        self.submit_button = Button(self.entry_error_frame, text="Submit", font="arial 14", command= self.to_check)
        self.submit_button.grid(row=0, column=1, padx=5)
       

        # Stats button to export results and a calculator (row 3)
        self.help_export_frame = Frame(self.quiz_frame, bg=back_ground)
        self.help_export_frame.grid(row=3)
        self.export_button = Button(self.help_export_frame, text="Quiz Stats", font="Arial 14 bold", bg="#003366", fg="white", command=self.export)
        self.export_button.grid(row=0, column=0, padx=5, pady=10)

     

        # Quit button
        self.quit_button = Button(self.help_export_frame, text="Quit", fg="white", width=10, bg="#660000", font="arial 14 bold", command=self.to_quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=10)

        if difficulty == 1:
            print("1")
            self.quiz_heading.config(text="Math Quiz: Easy")
            self.make_question(difficulty)
            
        
        elif difficulty == 2:
            print("2")
            self.quiz_heading.config(text="Math Quiz: Medium")
            self.make_question(difficulty)

        else:
            print("3")

    # closes program if user quits
    def to_quit(self):
        root.destroy()
    
    # generate export frame
    def export(self):
        get_export = Export(self)

    # generating addition and subtraction questions
    def make_question(self, fun):    

        # after making a new question, revert any color changes and clear entry box
        self.answer_entry.config(bg="white")
        self.answer_entry.delete(0, 'end')

        # generate operator and numbers for addition and subtraction
        operators = [('+', operator.add), ('-', operator.sub)]
        op, fn = random.choice(operators)
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        if num1 < num2:
            num1 = num1+num2
        correct_answer = fn(num1, num2)
        self.submit_button.config(command= lambda: self.to_check(num1, op, num2, correct_answer, fun))

        # config question to show numbers
        question_text = "{} {} {} = ?".format(num1, op, num2)
        self.question_label.config(text=question_text)

    # compares user answer with computed for easy difficulty
    def to_check(self, number1, oper, number2, sum_or_diff, difficulty):
        global score
        # solve and check
        answer = self.answer_entry.get()
        answer = int(answer)

        # if answer is wrong change bg to red to indicate it is wrong
        if answer != sum_or_diff:
            print("Incorrect")
            score -= difficulty
            self.question_label.config(text="{} {} {} = {}".format(number1, oper, number2, sum_or_diff))
            self.answer_entry.config(bg="#ffafaf")
        
        # if answer is correct change bg to green to indicate it is right
        else:
            print("Correct")
            score += difficulty
     
            self.answer_entry.config(bg="#98FB98")

        # freezes gui for about 2 seconds and then generate a new question
        self.quiz_score.config(text="Score: {}".format(score))
        self.question_label.after(1200, lambda: self.make_question(difficulty))   


class Help:
    def __init__(self, partner):

        # disable help button
        partner.help_button.config(state=DISABLED)

        # sets up child window (ie: help box)
        self.help_box = Toplevel()

        # if user presses cross at top, closes help and releases help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # set up GUI frame
        self.help_frame = Frame(self.help_box, width=300)
        self.help_frame.grid()

        # set up help heading
        self.how_heading = Label(self.help_frame, text="Help / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        help_text = "Select a difficulty level to start the quiz. The quiz is solely based on straight forward calculations so there are no word problems involved at all. Types of questions to expect for each level:\n\nEasy - Simple addition and subtraction questions a child could do\n\nMedium - Multiplication and division questions aimed for students around year 9 and 10\n\nHard - Solving for the area and perimeter of right-angled triangles, good luck :)"
        
        self.help_text = Label(self.help_frame, text=help_text, justify=LEFT, wrap=400, padx=10, pady=10)
        self.help_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="#660000", fg="white", font="arial 15 bold", command = partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        self.help_box.destroy()
        partner.help_button.config(state=NORMAL)
        root.deiconify()
    

class Draw:
    def __init__(self, partner):
        back = "light blue"
        root.withdraw()
        self.master_frame = Toplevel(bg=back, width=500, height=275)
        self.master_frame.grid()
        self.master_frame.config(bg="light blue")
        self.score_question_frame = Frame(self.master_frame, bg=back)
        self.score_question_frame.grid(row=0, padx=10, pady=10, sticky="NEWS")
        self.canvas = Canvas(self.master_frame)
        self.canvas.grid(row=1)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(back)
        self.to_draw = turtle.RawTurtle(self.screen)
        self.place_text = turtle.RawTurtle(self.screen)
        self.questions_frame = Frame(self.master_frame, bg=back)
        self.questions_frame.grid(row=2)

        # if users press cross at top, quiz quits
        self.master_frame.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.number_label = Label(self.score_question_frame, text="Question Number: {}".format(number), bg=back, font="arial 10 bold")
        self.number_label.grid(row=0, column=0, padx=10)
        self.question_label = Label(self.questions_frame, bg=back, text="Find the area and perimeter of the triangle below", font="arial 10 bold")
        self.question_label.grid(row=0, padx=10, pady=10, sticky="NEWS")

        self.user_lengths_label = Label(self.questions_frame, bg=back, justify=CENTER, font="arial 10 italic")
        self.user_lengths_label.grid(row=1, padx=10)

        # make entry labels and labels with a new frame
        self.area_perimeter_frame = Frame(self.master_frame, bg=back)
        self.area_perimeter_frame.grid(row=3)
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

        # make export frame and buttons
        self.export_quit_frame = Frame(self.master_frame, bg=back)
        self.export_quit_frame.grid(row=4)
        self.export_button = Button(self.export_quit_frame, width=10,  text="Quiz Stats", font="Arial 12 bold", bg="#003366", fg="white", command=self.export)
        self.export_button.grid(row=0, column=0, padx=5, pady=5)

        self.quit_button = Button(self.export_quit_frame, width=10,  bg="#660000", text="Quit", font="arial 12 bold", fg="white", command=self.to_quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=5)


        self.do_this()
    

    # create export window 
    def export(self):
        get_export = Export(self)

    # generate angles and a length
    def do_this(self):
        # generate angles and append to list
        a = random.randint(30, 80)
        b = 90 - a      # ensures triangle is always a right angle triangle
        some_angles.append(a)
        some_angles.append(b)

        # generate sides and append to list
        A = random.randint(10, 18)
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
        global score, number
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
                    self.perimeter_submit.config(state=DISABLED)
                    self.perimeter_entry.config(bg="#98FB98")
                    
            # if both area and perimeter answers are correct, generate a new question
            if self.perimeter_entry.cget("bg") == "#98FB98" and self.area_entry.cget("bg") == "#98FB98":
                print("Both are correct!")
                score += 2
                number += 1
                print(score, number)
                # reset lists and freeze canvas so user can see triangle before the reset
                self.perimeter_entry.after(1500, lambda e: e, self.perimeter_entry.delete(0, "end"))
                self.area_entry.after(1500, lambda e: e, self.area_entry.delete(0, "end"))
                some_angles.clear()
                some_sides.clear()
                
                # reset turtle screen
                self.screen.resetscreen()

                # change buttons back to normal and entry labels too
                self.number_label.config(text="Question number: {}".format(number))
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
    
    def to_quit(self):
        root.destroy()


class Export:
    
    def __init__(self, partner):
        background = "light blue"

        # disable export button
        partner.export_button.config(state=DISABLED)

        # sets up child window (ie: export box)
        self.export_box = Toplevel()

        # If users press cross at top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # set up GUI frame
        self.export_frame = Frame(self.export_box,  bg=background, width=300)
        self.export_frame.grid()

        # set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions", font=("Arial", "14", "bold"), bg=background)
        self.how_heading.grid(row=0)

        # export instructions (label, row 1)
        self.export_text = Label(self.export_frame, width=40, text="Enter a filename in the box below and press the Save button to save your calculation history to a text file", justify=LEFT, bg=background, wrap=250)
        self.export_text.grid(row=1)

        # warning text.. (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, its contents will be replaced with your calculation history", justify=LEFT, bg="#ffafaf", fg="maroon", font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)
       
        # filename entry box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # save / cancel frame
        self.save_cancel_frame = Frame(self.export_frame, bg="light blue")
        self.save_cancel_frame.grid(row=5, pady=10)

        # save and cancel buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font="arial 12 bold")
        self.save_button.grid(row=0, column=0, padx=10)

        # cancel button
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", font="arial 12 bold", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1, padx=10)

    def close_export(self, partner):
        # put export button back to normal...
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Math Quiz")
    something = Start(root)
    root.mainloop()