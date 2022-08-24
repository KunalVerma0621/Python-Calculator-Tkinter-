from tkinter import *
from ctypes import windll
import math

# variable
answer_for_global = ""
answer_for_sqrt = ""
answer_for_sqr = ""
answer_for_divide = ""

# colors
BLUE = "#6495ED"
WHITE = "#FDFEFE"
ORANGE = "#101820"
BLACK = "#F2AA4C"

# font style
FONT_STYLE = ("Arial", 18, "bold")
SMALL_FONT_STYLE = ("Arial", 25)
LARGE_FONT_STYLE = ("Arial", 30, "bold")


class Calculator(Tk):
    def __init__(self):
        super().__init__()
        self.value = ''
        self.iconbitmap('calculator_icon.ico')
        self.title("Calculator")
        self.geometry("600x800")
        self.minsize(width=500, height=700)
        self.total_expression = StringVar()
        self.current_expression = StringVar()
        self.display_frame = self.create_display_frame()
        self.total_label, self.current_label = self.create_display_label()
        self.icons = {"C": (1, 1), "x^2": (1, 2), "/x": (1, 3), "/": (1, 4),
                      "7": (2, 1), "8": (2, 2), "9": (2, 3), "*": (2, 4),
                      "4": (3, 1), "5": (3, 2), "6": (3, 3), "+": (3, 4),
                      "1": (4, 1), "2": (4, 2), "3": (4, 3), "-": (4, 4),
                      "0": (5, 1), ".": (5, 2), "%": (5, 3), "=": (5, 4)}
        self.button_frame = self.create_button_frame()
        for x in range(1, 5):
            self.button_frame.columnconfigure(x, weight=1)  # Button frame configure
            self.button_frame.rowconfigure(x, weight=1)
        self.create_special_button()
        self.columnconfigure(0, weight=1)    # root window configure
        self.rowconfigure(1, weight=1)
        self.bind_keys()

    # Take input from keyboard
    def bind_keys(self):
        self.bind('<Return>', lambda event: self.evaluate())
        for keys in self.icons:
            self.bind(keys, lambda event, key=keys: self.add_to_expression(key))

    # create answer frame upper
    def create_display_frame(self):
        display_frame = Frame(self, width=600, height=500)
        display_frame.grid(row=0, column=0, sticky=NSEW)
        return display_frame

    # create two frame inside answer frame
    def create_display_label(self):
        total_label = Label(self.display_frame, textvariable=self.total_expression, bg=ORANGE, fg=BLACK,
                            padx=10, font=SMALL_FONT_STYLE, height=3, anchor=E)
        total_label.pack(fill=BOTH, expand=True)

        current_label = Label(self.display_frame, textvariable=self.current_expression, bg=ORANGE, fg=BLACK,
                              padx=10, font=LARGE_FONT_STYLE, height=3, anchor=E)
        current_label.pack(fill=BOTH, expand=True)
        return total_label, current_label

    # Take value of button as expression and assigned in answer_for_global variable
    def add_to_expression(self, value):
        global answer_for_global
        global answer_for_sqrt
        global answer_for_sqr

        answer_for_global += str(value)
        answer_for_sqrt = answer_for_global
        answer_for_sqr = answer_for_global
        self.total_expression.set(answer_for_global)

    # create button in button frame lower
    def create_button_frame(self):
        button_frame = Frame(self, width=600, height=550)
        for icon, position in self.icons.items():
            b1 = Button(button_frame, text=icon, bg=BLACK, fg=ORANGE, width=4, height=3, font=FONT_STYLE,
                        borderwidth=0, command=lambda x=icon: self.add_to_expression(x), activebackground=BLACK,
                        activeforeground=ORANGE)
            b1.grid(row=position[0], column=position[1], sticky=NSEW)
        button_frame.grid(row=1, column=0, sticky=NSEW)
        return button_frame

    # call special button
    def create_special_button(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_divide_button()
        self.create_multiply_button()

    # clear the result
    def clear(self):
        global answer_for_global
        global answer_for_sqrt
        global answer_for_sqr
        answer_for_global = ""
        answer_for_sqrt = ""
        answer_for_sqr = ""
        self.total_expression.set('')
        self.current_expression.set('')

    # create clear button
    def create_clear_button(self):
        clear_button = Button(self.button_frame, text="C", bg=BLACK, fg=ORANGE, width=4, height=3,
                              font=FONT_STYLE, borderwidth=0, command=self.clear, activebackground=BLACK,
                              activeforeground=ORANGE)
        clear_button.grid(row=1, column=1, sticky=NSEW)

    # create divide button so that take / input from keyboard
    def create_divide_button(self):
        clear_button = Button(self.button_frame, text="\u00F7", bg=BLACK, fg=ORANGE, width=4, height=3,
                              font=FONT_STYLE, borderwidth=0, activebackground=BLACK, activeforeground=ORANGE,
                              command=lambda x="\u00F7": self.add_to_expression(x))
        clear_button.grid(row=1, column=4, sticky=NSEW)

    # create multiply button so that take * input from keyboard
    def create_multiply_button(self):
        clear_button = Button(self.button_frame, text="\u00D7", bg=BLACK, fg=ORANGE, width=4, height=3,
                              font=FONT_STYLE, borderwidth=0, activebackground=BLACK, activeforeground=ORANGE,
                              command=lambda x="\u00D7": self.add_to_expression(x))
        clear_button.grid(row=2, column=4, sticky=NSEW)

    # clear total expression after final answer generate
    def clear_total_expression(self):
        global answer_for_global
        global answer_for_sqrt
        global answer_for_sqr

        answer_for_sqrt = answer_for_global
        answer_for_sqr = answer_for_global
        answer_for_global = ""
        self.total_expression.set(answer_for_global)

    # evaluate the result of expression present in answer_for_global variable
    def evaluate(self):
        global answer_for_global
        global answer_for_divide
        answer_for_divide = answer_for_global
        answer_for_global = ""
        for i in answer_for_divide:
            if i == "\u00F7":
                i = '/'
                answer_for_global += i
            elif i == "\u00D7":
                i = '*'
                answer_for_global += i
            else:
                answer_for_global += i

        if answer_for_global == '':
            self.value = ''
        else:
            try:
                self.value = str(eval(answer_for_global))
                self.clear_total_expression()
                self.current_expression.set(self.value)
                if self.value == "0":
                    answer_for_global = ''
                else:
                    answer_for_global = self.value
            except SyntaxError:
                if self.value.isdigit():
                    self.current_expression.set(self.value)
                else:
                    self.clear_total_expression()
                    self.current_expression.set("Error")
            except ZeroDivisionError:
                self.current_expression.set("Cannot Divided by zero")
            except(ValueError, TypeError, NameError):
                self.clear_total_expression()
                self.current_expression.set("Error")

    # create equals button after user click = it will generate result
    def create_equals_button(self):
        equals_button = Button(self.button_frame, text="=", bg=BLACK, fg=ORANGE, width=4, height=3,
                               font=FONT_STYLE, borderwidth=0, command=self.evaluate, activebackground=BLACK,
                               activeforeground=ORANGE)
        equals_button.grid(row=5, column=4, sticky=NSEW)

    # evaluate the square of a digit
    def square(self):
        global answer_for_global
        global answer_for_sqr
        global answer_for_sqrt
        self.evaluate()
        try:
            answer_for_global = str(math.pow(eval(answer_for_sqr), 2))
            answer_for_sqr = answer_for_global
            answer_for_sqrt = answer_for_global
            self.current_expression.set(answer_for_global)
        except(ValueError, SyntaxError, TypeError, ZeroDivisionError):
            self.current_expression.set("Error")

    # create square button
    def create_square_button(self):
        square_button = Button(self.button_frame, text="x\u00b2", bg=BLACK, fg=ORANGE, width=4, height=3,
                               font=FONT_STYLE, borderwidth=0, command=self.square, activebackground=BLACK,
                               activeforeground=ORANGE)
        square_button.grid(row=1, column=2, sticky=NSEW)

    # evaluate the square_root of a digit
    def sqrt(self):
        global answer_for_global
        global answer_for_sqrt
        global answer_for_sqr
        self.evaluate()
        try:
            answer_for_global = str(math.sqrt(eval(answer_for_sqrt)))
            answer_for_sqrt = answer_for_global
            answer_for_sqr = answer_for_global
            self.current_expression.set(answer_for_global)
        except(ValueError, SyntaxError, TypeError, ZeroDivisionError):
            self.current_expression.set("Error")

    # create square_root button
    def create_sqrt_button(self):
        sqrt_button = Button(self.button_frame, text="\u221ax", bg=BLACK, fg=ORANGE, width=4, height=3,
                             font=FONT_STYLE, borderwidth=0, command=self.sqrt, activebackground=BLACK,
                             activeforeground=ORANGE)
        sqrt_button.grid(row=1, column=3, sticky=NSEW)


if __name__ == '__main__':
    c1 = Calculator()   # create the object of Calculator class
    windll.shcore.SetProcessDpiAwareness(1)   # decrease blur effect
    c1.mainloop()
