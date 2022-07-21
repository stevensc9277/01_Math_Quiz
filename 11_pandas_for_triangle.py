from tkinter import *
# randomly select operator (+, -, *, / )
import operator
from functools import partial
import random
import turtle
import math
import datetime as dt
import re 
import pandas

# lists for angles and sides
some_angles = []
some_sides = []
to_write = []

# variables to record number of questions answered right or wrong (easy and medium difficulty)
right = 0
wrong = 0

# record number of questions user has attempted to solve (number) and number of inconsistent tries made when solving for area / perimeter (tries)
number = 1
tries = 0

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

    # for hard difficulty, made a separate class and frame from medium and easy to avoid / reduce conflicting errors
    def to_draw(self):
        do_draw = Draw(self)


    def to_help(self):
        # redirect to a separate frame to give more detailed information of the game to user
        get_help = Help(self)
        root.withdraw()
    
    def to_quiz(self, difficulty):
        # redirect to quiz for easy and medium difficulty
        show_quiz = Quiz(self, difficulty)
        root.withdraw()


class Quiz:
    def __init__(self, partner, difficulty):
        # record score and stats here 
        self.score = 0
        self.quiz_stats = []
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

        # made a frame to show questions answered correctly and incorrectly. Appears at the top right corner of the quiz_frame (main frame)
        self.numbers_frame = Frame(self.quiz_frame, bg=back_ground)
        self.numbers_frame.grid(row=0, sticky=E)
        self.quiz_right = Label(self.numbers_frame, text="Right: 0", font="arial 11 italic", bg=back_ground)
        self.quiz_right.grid(row=0, sticky=E)
        self.quiz_wrong = Label(self.numbers_frame, text="Wrong: 0", font="arial 11 italic", bg=back_ground)
        self.quiz_wrong.grid(row=1, sticky=E)

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
        self.export_button = Button(self.help_export_frame, text="Quiz Stats", font="Arial 14 bold", bg="#003366", fg="white", command=lambda: self.export(self.quiz_stats, self.score))
        self.export_button.grid(row=0, column=0, padx=5, pady=10)

     

        # Quit button
        self.quit_button = Button(self.help_export_frame, text="Quit", fg="white", width=10, bg="#660000", font="arial 14 bold", command=self.to_quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=10)

        # easy difficulty, uses numbers 1 and 2 to determine whether to make addition/subtraction questions or multiplication/division questions
        if difficulty == 1:
            print("1")
            self.quiz_heading.config(text="Math Quiz: Easy")
            self.make_question(difficulty)
            
        # medium difficulty
        elif difficulty == 2:
            print("2")
            self.quiz_heading.config(text="Math Quiz: Medium")
            self.make_question(difficulty)

        # hard difficulty, pre triangle
        else:
            print("3")

    # closes program if user quits
    def to_quit(self):
        root.destroy()
    
    # generate export frame
    def export(self, quiz_history, score):
        self.quiz_box.withdraw()
        get_export = Export(self, quiz_history, score)

    # generating addition and subtraction questions
    def make_question(self, fun):    
        self.submit_button.config(state=NORMAL)
        # after making a new question, revert any color changes and clear entry box
        self.answer_entry.config(bg="white")
        self.answer_entry.delete(0, 'end')

        if fun == 1:
            # generate operator and numbers for addition and subtraction
            operators = [('+', operator.add), ('-', operator.sub)]
            op, fn = random.choice(operators)
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            if num1 < num2:
                num1 = num1+num2
            correct_answer = fn(num1, num2)
            self.submit_button.config(command= lambda: self.to_check(num1, op, num2, correct_answer, fun))

        else:
            # generate operator and numbers for multiplication and division
            # https://stackoverflow.com/questions/30926323/how-to-do-a-calculation-on-python-with-a-random-operator
            operators = [('x', operator.mul), ('/', operator.truediv)]
            op, fn = random.choice(operators)
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            if op == '/':
                num1 = random.randint(1, 12) * num2
            correct_answer = round(fn(num1, num2), 2)
            print(correct_answer)
            self.submit_button.config(command= lambda: self.to_check(num1, op, num2, correct_answer, fun))

        # config question to show numbers
        question_text = "{} {} {} = ?".format(num1, op, num2)
        self.question_label.config(text=question_text)

    # compares user answer with computed for easy difficulty
    def to_check(self, number1, oper, number2, sum_or_diff, difficulty):
        global right, wrong
        # solve and check
        
        try:
            answer = self.answer_entry.get()
            answer = float(answer)
            # if answer is wrong change bg to red to indicate it is wrong
            if answer != sum_or_diff:
                print("Incorrect")
                wrong += 1
                self.question_label.config(text="{} {} {} = {}".format(number1, oper, number2, sum_or_diff))
                self.answer_entry.config(bg="#ffafaf")
                self.quiz_stats.append("{} {} {} = {}       ||      Your answer was: {}".format(number1, oper, number2, sum_or_diff, answer))
            
            # if answer is correct change bg to green to indicate it is right
            else:
                print("Correct")
                right += 1
        
                self.answer_entry.config(bg="#98FB98")
        
        except ValueError:
            print("Incorrect")
            wrong += 1
            self.question_label.config(text="{} {} {} = {}".format(number1, oper, number2, sum_or_diff))
            self.answer_entry.config(bg="#ffafaf")
            self.quiz_stats.append("{} {} {} = {}       ||      Your answer was: {}".format(number1, oper, number2, sum_or_diff, answer))
        
        self.submit_button.config(state=DISABLED)
        self.score = (100*right)/(right+wrong)
        # freezes gui for about 2 seconds and then generate a new question
        self.quiz_right.config(text="Right: {}".format(right))
        self.quiz_wrong.config(text="Wrong: {}".format(wrong))
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

        # quiz instructions
        help_text = "Select a difficulty level to start the quiz. The quiz is solely based on straight forward calculations so there are no word problems involved at all. Types of questions to expect for each level:\n\nEasy - Simple addition and subtraction questions a child could do\n\nMedium - Multiplication and division questions aimed for students around year 9 and 10\n\nHard - Solving for the area and perimeter of right-angled triangles.You have 2 attempts at solving for either area / perimeter, after 2 attempts it is treated as you answering wrongly. Good luck :)"
        
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
        # closes previous window here, previously had an error where the triangle window would disappear after loading
        root.withdraw()

        # create and adjust main frame for turtle canvas
        self.master_frame = Toplevel(bg=back, width=500, height=275)
        self.master_frame.grid()
        self.master_frame.config(bg="light blue")

        # to show user how many questions they have answered
        self.score_question_frame = Frame(self.master_frame, bg=back)
        self.score_question_frame.grid(row=0, padx=10, pady=10, sticky="NEWS")

        # turtle canvas and screen
        self.canvas = Canvas(self.master_frame)
        self.canvas.grid(row=1)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor(back)

        # pens to draw turtle
        self.to_draw = turtle.RawTurtle(self.screen)
        self.place_text = turtle.RawTurtle(self.screen)

        self.questions_frame = Frame(self.master_frame, bg=back)
        self.questions_frame.grid(row=2)

        # use to format triangle data later
        anglength_dict = {
            'Angles': some_angles,
            'Angle_Names': ["ABC", "BCA", "CAB"],
            'Lengths': some_sides,
            'Lines': ["AB", "BC", "CA"]
            }
        # if users press cross at top, quiz ends
        self.master_frame.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.number_label = Label(self.score_question_frame, text="Question Number: {}".format(number), bg=back, font="arial 10 bold")
        self.number_label.grid(row=0, column=0, padx=10)
        self.question_label = Label(self.questions_frame, bg=back, text="Find the area and perimeter of the triangle below", font="arial 10 bold")
        self.question_label.grid(row=0, padx=10, pady=10, sticky="NEWS")

        self.user_lengths_label = Label(self.questions_frame, bg=back, justify=CENTER, font="arial 10 italic")
        self.user_lengths_label.grid(row=1, padx=10)

        # make entry labels with a new frame
        self.area_perimeter_frame = Frame(self.master_frame, bg=back)
        self.area_perimeter_frame.grid(row=3)
        self.area_label = Label(self.area_perimeter_frame, font="arial 13", text="Area", justify=LEFT, bg=back)
        self.area_label.grid(row=0, column=0, pady=10, padx=10, sticky="NEWS")
        self.area_entry = Entry(self.area_perimeter_frame, justify=CENTER, fg="grey")
        # inserts text into the entry label, does get removed
        self.area_entry.insert(0, "A = 0.5 x b x h")

        # bind commands, shows formulae if no input is detected or does nothing
        self.area_entry.bind("<FocusIn>", lambda e: self.on_enter(e, self.area_entry))
        self.area_entry.bind("<FocusOut>", lambda e: self.on_leave(e, self.area_entry))
        self.area_entry.grid(row=0, column=1, ipady=12, pady=5)

        self.perimeter_label = Label(self.area_perimeter_frame, font="arial 13", text="Perimeter", justify=LEFT, bg=back)
        self.perimeter_label.grid(row=1, column=0, padx=10, pady=10, sticky="NEWS")
        self.perimeter_entry = Entry(self.area_perimeter_frame, justify=CENTER, fg="grey")
        # inserts text into the entry label, does get removed
        self.perimeter_entry.insert(0, "P = AB + BC + CA")
        self.perimeter_entry.bind("<FocusIn>", lambda e: self.on_enter(e, self.perimeter_entry))
        self.perimeter_entry.bind("<FocusOut>", lambda e: self.on_leave(e, self.perimeter_entry))
        self.perimeter_entry.grid(row=1, column=1, padx=10, pady=10, ipady=12)

        # buttons to submit answers
        self.area_submit = Button(self.area_perimeter_frame, text="Submit", padx=10, pady=10, command= lambda: self.answer_check(self.area_entry, some_sides, anglength_dict))
        self.area_submit.grid(row=0, column=2)

        self.perimeter_submit = Button(self.area_perimeter_frame, text="Submit", padx=10, pady=10, command= lambda: self.answer_check(self.perimeter_entry, some_sides, anglength_dict))
        self.perimeter_submit.grid(row=1, column=2)

        # make export frame and buttons
        self.export_quit_frame = Frame(self.master_frame, bg=back)
        self.export_quit_frame.grid(row=4)
        self.export_button = Button(self.export_quit_frame, width=10,  text="Quiz Stats", font="Arial 12 bold", bg="#003366", fg="white", command=lambda: self.export(to_write))
        self.export_button.grid(row=0, column=0, padx=5, pady=5)

        self.quit_button = Button(self.export_quit_frame, width=10,  bg="#660000", text="Quit", font="arial 12 bold", fg="white", command=self.to_quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=5)


        self.do_this()
    

    # create export window 
    def export(self, history):
        get_export = Triangle_Export(self, history)
        self.master_frame.withdraw()

    # generate angles and a length
    def do_this(self):
        # generate angles and append to list
        a = random.randint(30, 80)
        # ensures triangle is always a right angle triangle
        b = 90 - a      
        some_angles.append(a)
        some_angles.append(b)

        # generate sides and append to list
        A = random.randint(10, 18)
        some_sides.append(A)

        self.finder(some_angles, some_sides)
       
    # changes entry label fg back to black and removes formulae
    def on_enter(self, e, name): 
        user_input = name.get()
        if user_input == "A = 0.5 x b x h" or user_input == "P = AB + BC + CA":
            name.delete(0, "end")
            name['foreground'] = 'black'

    # changes entry label fg back to black and shows formulae if there was no input given
    def on_leave(self, e, name):  
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

        # start drawing the triangle with given lengths and angles
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

    # solves for 2 uknown lengths
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
    
    def answer_check(self, name, lengths, anglength_dict):
        global tries, number, to_write
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
                    tries += 1
                    print(tries)
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
                    tries += 1
                    print(tries)
                    self.perimeter_entry.config(bg="#ffafaf")
                
                else:
                    self.perimeter_submit.config(state=DISABLED)
                    self.perimeter_entry.config(bg="#98FB98")
                    
            # if both area and perimeter answers are correct, generate a new question
            if self.perimeter_entry.cget("bg") == "#98FB98" and self.area_entry.cget("bg") == "#98FB98":
                print("Both are correct!")
                number += 1
                print(number)
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
                tries = 0
                self.do_this()  
                
            else:
                print("Something went wrong")
            
            if tries >= 2:
                ang_len_frame = pandas.DataFrame(anglength_dict)
                ang_len_frame = ang_len_frame.set_index('Angles')

                # Convert frames to strings
                ang_len_text = pandas.DataFrame.to_string(ang_len_frame)

                # export to file
                area = round(0.5 * lengths[0] * lengths[1], 2)
                perimeter = round(sum(lengths), 2)
                to_write.append(ang_len_text)
                to_write.append("The area was {}".format(area))
                to_write.append("The perimeter was {}".format(perimeter))
                to_write = list(dict.fromkeys(to_write))

        except ValueError:
            tries += 1
            name.delete(0, "end")
            name.config(bg="#ffafaf")
            name.insert(0, "Please enter a float")
            name.after(1500, lambda e: name.delete(0, "end"), name.config(bg="white"))
    
    def to_quit(self):
        root.destroy()


class Export:
    
    def __init__(self, partner, quiz_history, score):
        background = "#a9ef99"      # pale green
        score_percentage = score
    
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

        # Error message labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon", bg=background)
        self.save_error_label.grid(row=4)

        # save / cancel frame
        self.save_cancel_frame = Frame(self.export_frame, bg=background)
        self.save_cancel_frame.grid(row=5, pady=10)

        # save and cancel buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font="arial 12 bold", command=partial(lambda: self.save_history(partner, quiz_history, score_percentage)))
        self.save_button.grid(row=0, column=0, padx=10)

        # cancel button
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", font="arial 12 bold", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1, padx=10)

    
    def save_history(self, parent, quiz_history, score):
        # regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(no spaces allowed)"
                has_error = "yes"

            else:
                problem = ("(no {}'s allowed)".format(letter))
                has_error = "yes"
                break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            # Display error message
            self.save_error_label.config(text="Invalid filename - {}".format(problem))

            # change entry box background to pink
            self.filename_entry.config(bg="#ffafaf")
            print()
        
        else:
            # If there are no errrors, generate text file and then close dialogue box
            
            # change entry box color back to normal if no errors after previous error
            self.save_error_label.configure(text="", fg="blue")
            self.filename_entry.configure(bg="white")

            # add .txt suffix!
            filename = filename + ".txt"

            # create file to hold data
            f = open(filename, "w+")

            # find and return current date for testing purposes
            now = dt.datetime.now()

            # add new line at end of each item
            f.write("Questions answered incorrectly \t\t (Total Score: {}%)\n\n".format(score))
            f.write("Made on: " + now.strftime('%A, %B %d, %Y') + "\n\n")
            
            if score == 100:
                f.write("Congratulations! You answered every question correctly")
            
            elif score <= 50:
                f.write("You should study more maths\n\n")

            for item in quiz_history:
                f.write(item + "\n")

            # close file
            f.close()
            self.close_export(parent)
            self.export_box.destroy()
            

    def close_export(self, partner):
        # put export button back to normal...
        partner.quiz_box.deiconify()
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()
   

class Triangle_Export:
    
    def __init__(self, partner, quiz_history):
        background = "#a9ef99"      # pale green
    
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

        # Error message labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon", bg=background)
        self.save_error_label.grid(row=4)

        # save / cancel frame
        self.save_cancel_frame = Frame(self.export_frame, bg=background)
        self.save_cancel_frame.grid(row=5, pady=10)

        # save and cancel buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font="arial 12 bold", command=partial(lambda: self.save_history(partner, quiz_history)))
        print(quiz_history)
        self.save_button.grid(row=0, column=0, padx=10)

        # cancel button
        self.cancel_button = Button(self.save_cancel_frame, text="Cancel", font="arial 12 bold", command=partial(self.close_export, partner))
        self.cancel_button.grid(row=0, column=1, padx=10)

    
    def save_history(self, parent, quiz_history):
        # regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "(no spaces allowed)"
                has_error = "yes"

            else:
                problem = ("(no {}'s allowed)".format(letter))
                has_error = "yes"
                break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            # Display error message
            self.save_error_label.config(text="Invalid filename - {}".format(problem))

            # change entry box background to pink
            self.filename_entry.config(bg="#ffafaf")
            print()
        
        else:
            # If there are no errrors, generate text file and then close dialogue box
            
            # change entry box color back to normal if no errors after previous error
            self.save_error_label.configure(text="", fg="blue")
            self.filename_entry.configure(bg="white")

            # add .txt suffix!
            filename = filename + ".txt"

            # create file to hold data
            f = open(filename, "w+")

            # find and return current date for testing purposes
            now = dt.datetime.now()

            # add new line at end of each item
            f.write("Questions answered incorrectly\n\n")
            f.write("Made on: " + now.strftime('%A, %B %d, %Y') + "\n\n")
            
            # if list (quiz_history) has items, print them
            if quiz_history:
                for item in quiz_history:
                    f.write(str(item))
                    f.write("\n\n")
            
            # if list is empty / False, print something else ----> no questions answered with more than 3 attempts
            else:
                f.write("You answered every question correctly")
                
            # close file
            f.close()
            self.close_export(parent)
            self.export_box.destroy()
            

    def close_export(self, partner):
        # put export button back to normal...
        partner.master_frame.deiconify()
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()
   
# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Math Quiz")
    something = Start(root)
    root.mainloop()