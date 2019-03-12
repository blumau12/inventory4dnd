from tkinter import *


def button_description(button, text, self):
    event = None
    self.search_description_top = None
    button.bind("<Button-1>", lambda event=event: search_description(self, text, button, True))
    button.bind("<Leave>", lambda event=event: search_description(self, text, button, False))


def search_description(self, text, button, turn_on, event=None):
    if turn_on:
        if not self.search_description_top and text:
            self.search_description_top = Toplevel()
            self.search_description_top.wm_overrideredirect(True)
            self.search_description_top_label = Label(self.search_description_top,
                                                      text=text, justify=LEFT,
                                                      background="#f7f7f7", relief=SOLID,
                                                      borderwidth=1, font='Cambria 12')
            self.search_description_top_label.grid(row=0, column=0)
            x = button.winfo_rootx() - int(len(
                self.search_description_top_label.cget("text")) * 3.5) + int(button.winfo_width() / 2)
            y = button.winfo_rooty() + 20
            self.search_description_top.geometry("+%s+%s" % (x, y))
            return event
    else:
        try:
            self.search_description_top.destroy()
            self.search_description_top = None
        except AttributeError:
            pass
        return event
