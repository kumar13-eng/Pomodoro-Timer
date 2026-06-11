from tkinter import *
import math
import os

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=YELLOW)
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        count_down(long_break)
        title_label.config(text="Break ", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break)
        title_label.config(text="Break ", fg=GREEN)
    else:
        count_down(work_sec)
        title_label.config(text="Work ", fg=YELLOW)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec == 0:
        count_sec = "00"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.configure(bg=PINK)
window.config(padx=100, pady=50)

title_label = Label(text="Timer", fg=YELLOW, bg=PINK, font=(FONT_NAME, 50))
title_label.grid(row=0, column=1)

canvas = Canvas(height=224, width=200, bg=PINK, highlightthickness=0)
script_dir = os.path.dirname(os.path.abspath(__file__))
tomato_path = os.path.join(script_dir, "tomato.png")
try:
    tomato_img = PhotoImage(file=tomato_path)
    canvas.create_image(100, 112, image=tomato_img)
except Exception:
    tomato_img = None
    canvas.create_oval(25, 37, 175, 187, fill=RED, outline=RED)
    canvas.create_oval(80, 5, 120, 35, fill=GREEN, outline=GREEN)
    canvas.create_line(100, 5, 90, 25, fill=GREEN, width=5)
    canvas.create_line(100, 5, 110, 25, fill=GREEN, width=5)

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

start_button = Button(text="start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="reset", highlightthickness=0,command=reset_timer)
reset_button.grid(row=2, column=2)

check_marks = Label(fg=GREEN, bg=PINK)
check_marks.grid(row=3, column=1)
window.mainloop()
