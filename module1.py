import tkinter as tk
from tkinter import ttk
import sqlite3

# Функция создания базы данных и таблиц
def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Создание таблицы Авторы
    c.execute('''CREATE TABLE IF NOT EXISTS Authors
                 (author_id INTEGER PRIMARY KEY,
                  author_name TEXT NOT NULL,
                  birth_date TEXT)''')

    # Создание таблицы Жанры
    c.execute('''CREATE TABLE IF NOT EXISTS Genres
                 (genre_id INTEGER PRIMARY KEY,
                  genre_name TEXT NOT NULL)''')

    # Создание таблицы Книги
    c.execute('''CREATE TABLE IF NOT EXISTS Books
                 (book_id INTEGER PRIMARY KEY,
                  title TEXT NOT NULL,
                  publication_date TEXT,
                  author_id INTEGER,
                  genre_id INTEGER,
                  FOREIGN KEY (author_id) REFERENCES Authors(author_id),
                  FOREIGN KEY (genre_id) REFERENCES Genres(genre_id))''')

    conn.commit()
    conn.close()

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление библиотекой")

        # Создание соединения с базой данных
        self.conn = sqlite3.connect('library.db')
        self.c = self.conn.cursor()

        # Создание виджетов
        self.book_frame = ttk.LabelFrame(root, text="Книги")
        self.book_frame.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.author_frame = ttk.LabelFrame(root, text="Авторы")
        self.author_frame.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.genre_frame = ttk.LabelFrame(root, text="Жанры")
        self.genre_frame.grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)

        self.book_listbox = tk.Listbox(self.book_frame, width=50)
        self.book_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.author_listbox = tk.Listbox(self.author_frame, width=30)
        self.author_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.genre_listbox = tk.Listbox(self.genre_frame, width=30)
        self.genre_listbox.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        # Заполнение списков данными из базы данных
        self.populate_book_list()
        self.populate_author_list()
        self.populate_genre_list()

    def populate_book_list(self):
        self.book_listbox.delete(0, tk.END)
        books = self.c.execute('''SELECT title FROM Books''').fetchall()
        for book in books:
            self.book_listbox.insert(tk.END, book[0])

    def populate_author_list(self):
        self.author_listbox.delete(0, tk.END)
        authors = self.c.execute('''SELECT author_name FROM Authors''').fetchall()
        for author in authors:
            self.author_listbox.insert(tk.END, author[0])

    def populate_genre_list(self):
        self.genre_listbox.delete(0, tk.END)
        genres = self.c.execute('''SELECT genre_name FROM Genres''').fetchall()
        for genre in genres:
            self.genre_listbox.insert(tk.END, genre[0])

create_database()  # Создание базы данных и таблиц перед запуском приложения

root = tk.Tk()
app = LibraryManagementApp(root)
root.mainloop()

