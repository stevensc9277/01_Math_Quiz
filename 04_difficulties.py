from tkinter import *
# randomly select operator (+, -, *, / )
import operator
from functools import partial
import random


score = 0
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
        self.easy_button = Button(self.button_frame, text="Easy", font="Arial 12 italic", command=lambda: self.to_quiz(1))
        self.easy_button.grid(row=0, column=0, padx=10, pady=10)

        self.medium_button = Button(self.button_frame, text="Medium", font="Arial 12 italic", command=lambda: self.to_quiz(2))
        self.medium_button.grid(row=0, column=1, padx=10, pady=10)

        self.hard_button = Button(self.button_frame, text="Hard", font="Arial 12 italic", command=lambda: self.to_quiz(3))
        self.hard_button.grid(row=0, column=2, padx=10, pady=10)

        # help button (row 3)
        self.help_button = Button(self.start_frame, text="Help", font="Arial 12", command=self.to_help)
        self.help_button.grid(row=3, padx=10, pady=10)

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
        self.quiz_heading = Label(self.quiz_frame, text="Math Quiz", justify=LEFT, font="arial 14 bold", bg=back_ground)
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

        self.error_entry = Label(self.quiz_frame, font="Arial 12 bold", bg=back_ground, wrap=250)
        self.error_entry.grid(row=3, padx=5, pady=5)
      

        # Stats button to export results and a calculator (row 3)
        self.help_export_frame = Frame(self.quiz_frame, bg=back_ground)
        self.help_export_frame.grid(row=4)
        self.stats_button = Button(self.help_export_frame, text="Quiz Stats", font="Arial 14 bold", bg="#003366", fg="white")
        self.stats_button.grid(row=0, column=0, padx=5, pady=10)

     

        # Quit button
        self.quit_button = Button(self.help_export_frame, text="Quit", fg="white", width=10, bg="#660000", font="arial 14 bold", command=self.to_quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=10)

        if difficulty == 1:
            print("Selected easy difficulty")
            self.make_question(1)
            
        
        elif difficulty == 2:
            print("Selected medium difficulty")
            self.make_question(2)

        else:
            print("Selected hard difficulty")

    def to_quit(self):
        root.destroy()
    
    def make_question(self, difficulty):

        # after making a new question, revert any color changes and clear entry box
        self.answer_entry.config(bg="white")
        self.answer_entry.delete(0, 'end')
        self.error_entry.config(text="")

        # depending on difficulty level, adjust questions to match skill
        if difficulty == 1:
            operators = [('+', operator.add), ('-', operator.sub)]
            op, fn = random.choice(operators)
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            if num1 < num2:
                num1 = num1+num2
            correct_answer = fn(num1, num2)
            self.submit_button.config(command= lambda: self.to_check(difficulty, num1, op, num2, correct_answer))

        elif difficulty == 2:
            operators = [('x', operator.mul), ('/', operator.truediv)]
            op, fn = random.choice(operators)
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
            # decided to round quotients to 2dp as it is more accurate than 1dp and easier to work out
            correct_answer = round(fn(num1, num2), 2)
            self.submit_button.config(command= lambda: self.to_check(difficulty, num1, op, num2, correct_answer))

        # config question to show numbers
        question_text = "{} {} {} = ?".format(num1, op, num2)
        self.question_label.config(text=question_text)
          # bind entry label to enter key (<Return>)
        self.answer_entry.bind('<Return>', lambda e: self.to_check(difficulty, num1, op, num2, correct_answer))
       

    # compares user answer with computed
    def to_check(self, difficulty, number1, oper, number2, result):
        global score
        # solve and check
        answer = self.answer_entry.get()

        try:
            answer = float(answer)
            

            # if answer is wrong change bg to red to indicate it is wrong
            if answer != result:
                print("Incorrect")
                score -= difficulty
                self.question_label.config(text="{} {} {} = {}".format(number1, oper, number2, result))
                self.answer_entry.config(bg="#ffafaf")
            
            # if answer is correct change bg to green to indicate it is right
            else:
                print("Correct")
                score += difficulty
                self.answer_entry.config(bg="#98FB98")

            # freezes gui for about 2 seconds and then generate a new question
            self.quiz_score.config(text="Score: {}".format(score))
            self.question_label.after(1500, lambda: self.make_question(difficulty))   

        except ValueError:
            print("Incorrect, bad input detected")
            self.question_label.config(text="{} {} {} = {}".format(number1, oper, number2, result))
            self.answer_entry.config(bg="#ffafaf")
            self.error_entry.config(text="Please use numbers to answer the questions", fg="red")
            self.quiz_score.config(text="Score: {}".format(score))
            self.question_label.after(1500, lambda: self.make_question(difficulty))  

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

        help_text = "Select a difficulty level to start the quiz. The quiz is solely based on straight forward calculations so there are no word problems involved at all. Types of questions to expect for each level:\n\nEasy - Simple addition and subtraction questions a child could do\n\nMedium - Multiplication and division questions aimed for students with possible logarithmic questions mixed in\n\nHard - Just year 12 calculus stuff\n\nThere is a calculator available to use for some simple calculations, good luck :)"
        
        self.help_text = Label(self.help_frame, text=help_text, justify=LEFT, wrap=400, padx=10, pady=10)
        self.help_text.grid(row=1)

        # dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="#660000", fg="white", font="arial 15 bold", command = partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        self.help_box.destroy()
        partner.help_button.config(state=NORMAL)
        root.deiconify()
    

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Math Quiz")
    something = Start(root)
    root.mainloop()