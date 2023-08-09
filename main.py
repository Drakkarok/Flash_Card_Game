import tkinter
import pandas
import os
import random
import sys

BACKGROUND_COLOR = "#B1DDC6"

try:
    df = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = df = pandas.read_csv('./data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas_for_card.itemconfig(card_title, text="French", fill="black")
    canvas_for_card.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas_for_card.itemconfig(card_background, image=card_image_front)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas_for_card.itemconfig(card_title, text="English", fill="white")
    canvas_for_card.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas_for_card.itemconfig(card_background, image=card_image_back)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def reset():
    os.remove("./data/words_to_learn.csv")
    os.spawnv(os.P_NOWAIT, sys.executable, [sys.executable, "main.py"])
    window.quit()

# ------------------------------------------ UI SETUP ------------------------------------------ #


# --- window ---
window = tkinter.Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# --- card paths ---
card_image_front = tkinter.PhotoImage(file=os.path.abspath("./images/card_front.png"))
card_image_back = tkinter.PhotoImage(file=os.path.abspath("./images/card_back.png"))
current_face = card_image_front

# --- canvas for cards ---
canvas_for_card = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas_for_card.create_image(400, 263, image=card_image_front)
canvas_for_card.grid(column=0, row=0, columnspan=5)
card_title = canvas_for_card.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_text = canvas_for_card.create_text(400, 263, text="Flash Card!", font=("Arial", 60, "bold"))

next_card()

# ---------------------- BUTTONS ----------------------
cross_image = tkinter.PhotoImage(file=os.path.abspath("./images/wrong.png"))
check_image = tkinter.PhotoImage(file=os.path.abspath("./images/right.png"))

unknown_button = tkinter.Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=1, row=1)

known_button = tkinter.Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(column=3, row=1)

reset_button = tkinter.Button(text="Reset", highlightthickness=0, command=reset)
reset_button.grid(column=2, row=1)

window.mainloop()


