from tkinter import * 

root = Tk()
root.geometry("600x600")
button = Button(root, text="Click here", command=lambda: button.config(state=DISABLED))
button.grid()
button.bind('<Return>', lambda e: button.config(state=NORMAL))



root.mainloop()