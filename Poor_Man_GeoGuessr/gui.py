import time
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from main import Database, Query, Coord, Csv_row, Result
from getpass import getpass


class Application(tk.Frame):
    def __init__(self, root, db, query):
        super().__init__(root)
        self.root = root
        self._user_selection = tk.StringVar(self)
        self._db = db
        self._query = query
        self.score = 0
        self.pack()
        self.create_widgets()
        self.new_round()

    def exit_with_message(self, message):
        messagebox.showwarning(message=message)
        self.root.destroy()
        raise RuntimeError(message)

    def get_new_coordinate(self):
        num_retries = 0
        while True:
            if num_retries >= 3:
                self.exit_with_message('Too many retries. Exiting.')
            try:
                csv_row = self._db.get_csv_row()
            except IndexError:
                self.exit_with_message('You have played all the locations available.')
            result = self._query.download(csv_row.coord)
            if result == Result.OK:
                break
            elif result == Result.RETRY:
                print(f'Failed getting {csv_row}, retrying next one.')
                time.sleep(1)
                num_retries += 1
            elif result == Result.ERROR:
                self.exit_with_message(f"Something happened and we cannot fix it. {csv_row}")
        self.answer = csv_row.country_name

    def new_round(self):
        self.set_score_board()
        self._user_selection.set("")
        self.dropdown.update()
        self.img.configure(image="", width=640*4, height=640)
        self.get_new_coordinate()
        self.load_images()

    def submit(self):
        user_selection = self._user_selection.get()
        if user_selection == self.answer:
            self.score += 1
            messagebox.showinfo(message=f"Correct! You have {self.score} points now!")
        else:
            self.score = 0
            messagebox.showinfo(message=f"Wrong! The correct answer is {self.answer}. Your score has been reset.")
        self.new_round()

    def load_images(self):
        image = Image.new('RGBA', (640*4, 640))
        for i in range(4):
            image.paste(Image.open(f'downloads/gsv_{i}.jpg'), (640*i, 0))
        image = ImageTk.PhotoImage(image)
        self.img.configure(image=image)
        self.img.image = image

    def set_score_board(self):
        self.score_board.configure(text=f"score: {self.score}")

    def create_widgets(self):
        self.img = tk.Label(self, width=640*4, height=640)
        self.img.pack(side="top")
        options = self._db.get_all_countries()
        self.dropdown = ttk.OptionMenu(self, self._user_selection, None, *options)
        self.dropdown.pack(side="top")
        self.submit = tk.Button(self, text="SUBMIT", command=self.submit)
        self.submit.pack(side="top")
        self.score_board = tk.Label(self)
        self.score_board.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.quit.pack(side="top")


def main(key):
    root = tk.Tk()
    root.geometry('2580x800')
    database = Database('coordinates.csv')
    query = Query(key)
    app = Application(root, database, query)
    app.mainloop()


if __name__ == '__main__':
    key = getpass("Enter your key: ")
    main(key)
