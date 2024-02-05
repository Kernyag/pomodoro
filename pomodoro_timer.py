from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
reps = 0
check = ""
timer = None
is_pause = False
time_left = 0


# ---------------------------- TIMER PAUSE ------------------------------- #

def pause_timer():
    global is_pause
    window.after_cancel(timer)
    is_pause = True


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, check
    window.after_cancel(timer)
    reps = 0
    check = ""
    timer_label.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")
    canvas.itemconfig(timer_text, text="00:00")


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, is_pause
    if is_pause:
        if reps == 0:
            reps += 1
        is_pause = False
        work_sec = time_left
        short_break_sec = time_left
        long_brake_sec = time_left
    else:
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_brake_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_brake_sec)
        timer_label.config(text="Brake", fg=RED)
        window.attributes('-topmost', 1)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        timer_label.config(text="Brake", fg=PINK)
        window.attributes('-topmost', 1)
    else:
        timer_label.config(text="Work", fg=GREEN)
        count_down(work_sec)
        window.attributes('-topmost', 0)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global check, timer, time_left
    min = int(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    if min < 10:
        min = f"0{min}"
    canvas.itemconfig(timer_text, text=f"{min}:{seconds}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
        time_left = count
        if time_left < 60:
            window.attributes('-topmost', 1)
    else:
        start_timer()
        if reps % 2 == 0:
            check += "✔"
            checkmark_label.config(text=check)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
# colorhunt
window.config(padx=100, pady=50, bg=YELLOW)
window.title("POMODORO")

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

# Labels
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
timer_label.grid(column=1, row=0)

checkmark_label = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15, "bold"))
checkmark_label.grid(column=1, row=3)

# Buttons
start_bt = Button(text="Start", width=7, command=start_timer)
start_bt.grid(column=0, row=2)

reset_bt = Button(text="Reset", width=7, command=reset_timer)
reset_bt.grid(column=3, row=2)

pause_bt = Button(text="Pause", width=7, command=pause_timer)
pause_bt.grid(column=3, row=3)

window.mainloop()
