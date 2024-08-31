import random
import pandas
from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

try:
    file = open('data/words_to_learn.csv')
except FileNotFoundError:
    data = pandas.read_csv('data/japanese_words.csv')
    words = data.to_dict(orient='records')
else:
    file.close()
    words = pandas.read_csv('data/words_to_learn.csv').to_dict(orient='records')

current_word = {}


def generate_word(is_correct = False):
    global current_word, flip_timer
    current_word = random.choice(words)
    window.after_cancel(flip_timer)
    canvas.itemconfigure(card_title, fill='black')
    canvas.itemconfigure(card_word, fill='black')
    canvas.itemconfigure(card_title, text='Japanese')
    canvas.itemconfigure(card_word, text=current_word.get('japanese'))
    canvas.itemconfigure(card_background, image=card_front_image)
    if is_correct:
        words.remove(current_word)
    flip_timer = window.after(ms=3000, func=flip_flash_card)


def flip_flash_card():
    canvas.itemconfigure(card_title, fill='white')
    canvas.itemconfigure(card_word, fill='white')
    canvas.itemconfigure(card_title, text='English')
    canvas.itemconfigure(card_word, text=current_word.get('english'))
    canvas.itemconfigure(card_background, image=card_back_image)


window = Tk()
flip_timer = window.after(ms=5000, func=flip_flash_card)
window.title('Fancy flash cards')
window.configure(background=BACKGROUND_COLOR, padx=50, pady=50)

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
check_mark_image = PhotoImage(file="images/right.png")
cross_mark_image = PhotoImage(file="images/wrong.png")

canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400, 150, font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, font=('Ariel', 80, 'bold'), tag='word')

correct_button = Button(image=check_mark_image, highlightthickness=0, command=lambda: generate_word(True))
correct_button.grid(row=1, column=0)

wrong_button = Button(image=cross_mark_image, highlightthickness=0, command=lambda: generate_word(False))
wrong_button.grid(row=1, column=1)

generate_word()

window.mainloop()

try:
    file = open(file="data/words_to_learn.csv")
except FileNotFoundError:
    file = open(file="data/words_to_learn.csv", mode='w')
    file.close()
finally:
    data_frame = pandas.DataFrame(words)
    data_frame.to_csv("data/words_to_learn.csv", index=False, header=True)
