import tkinter as tk

root = tk.Tk()
e = tk.Entry(root, fg='grey')
e.insert(0, "some text")


def some_callback(event):  # must include event
    e.delete(0, "end")
    e['foreground'] = 'black'
    # e.unbind("<Button-1>")
    e.unbind("<FocusIn>")

    return None


# e.bind("<Button-1>", some_callback)
e.bind("<FocusIn>", some_callback)

e.pack()

root.mainloop()