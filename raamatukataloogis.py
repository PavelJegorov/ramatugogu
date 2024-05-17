import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Определение функций работы с базой данных

def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS Authors
                 (author_id INTEGER PRIMARY KEY,
                  author_name TEXT NOT NULL,
                  birth_date TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Genres
                 (genre_id INTEGER PRIMARY KEY,
                  genre_name TEXT NOT NULL)''')
    
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

def insert_author(author_name, birth_date):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO Authors (author_name, birth_date) 
                 VALUES (?, ?)''', (author_name, birth_date))
    
    conn.commit()
    conn.close()

def insert_genre(genre_name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO Genres (genre_name) 
                 VALUES (?)''', (genre_name,))
    
    conn.commit()
    conn.close()

def insert_book(title, publication_date, author_id, genre_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO Books (title, publication_date, author_id, genre_id) 
                 VALUES (?, ?, ?, ?)''', (title, publication_date, author_id, genre_id))
    
    conn.commit()
    conn.close()

def get_books_with_author_and_genre():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute('''SELECT Books.title, Authors.author_name, Genres.genre_name
                 FROM Books
                 LEFT JOIN Authors ON Books.author_id = Authors.author_id
                 LEFT JOIN Genres ON Books.genre_id = Genres.genre_id''')
    
    books = c.fetchall()
    
    conn.close()
    
    return books

def delete_book(book_title):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute("SELECT book_id FROM Books WHERE title=?", (book_title,))
    book_id = c.fetchone()
    
    if book_id:
        book_id = book_id[0]
        c.execute("DELETE FROM Books WHERE book_id=?", (book_id,))
    
    conn.commit()
    conn.close()

def delete_author(author_name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute("SELECT author_id FROM Authors WHERE author_name=?", (author_name,))
    author_id = c.fetchone()
    
    if author_id:
        author_id = author_id[0]
        c.execute("UPDATE Books SET author_id=NULL WHERE author_id=?", (author_id,))
        c.execute("DELETE FROM Authors WHERE author_id=?", (author_id,))
    
    conn.commit()
    conn.close()

def delete_genre(genre_name):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    c.execute("SELECT genre_id FROM Genres WHERE genre_name=?", (genre_name,))
    genre_id = c.fetchone()
    
    if genre_id:
        genre_id = genre_id[0]
        c.execute("UPDATE Books SET genre_id=NULL WHERE genre_id=?", (genre_id,))
        c.execute("DELETE FROM Genres WHERE genre_id=?", (genre_id,))
    
    conn.commit()
    conn.close()

# Определение класса для управления библиотекой

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление библиотекой")

        create_database()

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

        ttk.Label(self.book_frame, text="Название книги:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.book_title_entry = ttk.Entry(self.book_frame, width=40)
        self.book_title_entry.grid(row=1, column=1, padx=5, pady=5,sticky=tk.W)

        ttk.Label(self.book_frame, text="Дата публикации:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.publication_date_entry = ttk.Entry(self.book_frame, width=40)
        self.publication_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.book_frame, text="Автор:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.author_entry = ttk.Entry(self.book_frame, width=40)
        self.author_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.book_frame, text="Жанр:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.genre_entry = ttk.Entry(self.book_frame, width=40)
        self.genre_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_book_button = ttk.Button(self.book_frame, text="Добавить книгу", command=self.add_book)
        self.add_book_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.delete_book_button = ttk.Button(self.book_frame, text="Удалить книгу", command=self.delete_book)
        self.delete_book_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.add_author_button = ttk.Button(self.author_frame, text="Добавить автора", command=self.add_author)
        self.add_author_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.add_genre_button = ttk.Button(self.genre_frame, text="Добавить жанр", command=self.add_genre)
        self.add_genre_button.grid(row=1, column=0, columnspan=2, pady=5)

        self.delete_author_button = ttk.Button(self.author_frame, text="Удалить автора", command=self.delete_author)
        self.delete_author_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.delete_genre_button = ttk.Button(self.genre_frame, text="Удалить жанр", command=self.delete_genre)
        self.delete_genre_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.populate_author_list()
        self.populate_genre_list()
        self.populate_book_list()

    def add_book(self):
        title = self.book_title_entry.get()
        publication_date = self.publication_date_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        
        if not title or not publication_date or not author or not genre:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля!")
            return
        
        author_id = self.get_author_id(author)
        if not author_id:
            insert_author(author, "")
            author_id = self.get_author_id(author)
        
        genre_id = self.get_genre_id(genre)
        if not genre_id:
            insert_genre(genre)
            genre_id = self.get_genre_id(genre)
        
        insert_book(title, publication_date, author_id, genre_id)
        
        self.populate_author_list()
        self.populate_genre_list()
        self.populate_book_list()
        
        self.book_title_entry.delete(0, tk.END)
        self.publication_date_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)

    def add_author(self):
        author = self.author_entry.get()
        
        if not author:
            messagebox.showerror("Ошибка", "Пожалуйста, введите имя автора!")
            return
        
        insert_author(author, "")
        self.populate_author_list()
        self.author_entry.delete(0, tk.END)

    def add_genre(self):
        genre = self.genre_entry.get()
        
        if not genre:
            messagebox.showerror("Ошибка", "Пожалуйста, введите название жанра!")
            return
        
        insert_genre(genre)
        self.populate_genre_list()
        self.genre_entry.delete(0, tk.END)

    def delete_book(self):
        selected_book = self.book_listbox.get(tk.ACTIVE)
        if not selected_book:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите книгу для удаления!")
            return
        
        book_title = selected_book.split(" - ")[0]
        delete_book(book_title)
        
        self.populate_author_list()
        self.populate_genre_list()
        self.populate_book_list()

    def delete_author(self):
        selected_author = self.author_listbox.get(tk.ACTIVE)
        if not selected_author:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите автора для удаления!")
            return
        
        delete_author(selected_author)
        self.populate_author_list()
        self.populate_genre_list()
        self.populate_book_list()

    def delete_genre(self):
        selected_genre = self.genre_listbox.get(tk.ACTIVE)
        if not selected_genre:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите жанр для удаления!")
            return
        
        delete_genre(selected_genre)
        self.populate_author_list()
        self.populate_genre_list()
        self.populate_book_list()

    def populate_author_list(self):
        self.author_listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT author_name FROM Authors")
        authors = c.fetchall()
        conn.close()
        
        for author in authors:
            self.author_listbox.insert(tk.END, author[0])

    def populate_genre_list(self):
        self.genre_listbox.delete(0, tk.END)
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT genre_name FROM Genres")
        genres = c.fetchall()
        conn.close()
        
        for genre in genres:
            self.genre_listbox.insert(tk.END, genre[0])

    def populate_book_list(self):
        self.book_listbox.delete(0, tk.END)
        books = get_books_with_author_and_genre()
        
        for book in books:
            self.book_listbox.insert(tk.END, f"{book[0]} - {book[1]} ({book[2]})")

    def get_author_id(self, author_name):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT author_id FROM Authors WHERE author_name=?", (author_name,))
        author_id = c.fetchone()
        conn.close()
        return author_id[0] if author_id else None

    def get_genre_id(self, genre_name):
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("SELECT genre_id FROM Genres WHERE genre_name=?", (genre_name,))
        genre_id = c.fetchone()
        conn.close()
        return genre_id[0] if genre_id else None

root = tk.Tk()
app = LibraryManagementApp(root)
root.mainloop()

