import tkinter as tk


class Btn(tk.Button):
    def __init__(self, root, text, color, command, **kwargs):
        palette = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'F']
        active = '#'
        for i in range(1, 4):
            active += palette[palette.index(color[i].upper()) + 1]
        super().__init__(master=root, text=text, relief=tk.GROOVE, bg=color, activebackground=active, command=command,
                         **kwargs)
