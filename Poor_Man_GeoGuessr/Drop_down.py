import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv

app = tk.Tk()
app.geometry('200x100')

labelTop = tk.Label(app)
labelTop.grid(column=0, row=0)
labelTop.configure(image='')

image = Image.open(f'downloads/gsv_0.jpg')
image = ImageTk.PhotoImage(image)
labelTop.configure(image=image, text='')


app.mainloop()
