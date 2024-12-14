import sqlite3
import tkinter as tk
from tkinter import messagebox


# Функция для создания базы данных и таблицы пользователей
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Функция для регистрации пользователя
def register_user():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    if not username or not password:
        messagebox.showwarning("Предупреждение", "Пожалуйста, заполните все поля.")
        return

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Успех", "Пользователь зарегистрирован!")
        registration_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Такой логин уже существует.")

    conn.close()


# Функция для авторизации
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Успех", "Авторизация прошла успешно!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    conn.close()


# Функция для открытия окна регистрации
def open_registration_window():
    global registration_window, reg_username_entry, reg_password_entry
    registration_window = tk.Toplevel()
    registration_window.title("Регистрация")

    tk.Label(registration_window, text="Логин").pack(pady=5)
    reg_username_entry = tk.Entry(registration_window)
    reg_username_entry.pack(pady=5)

    tk.Label(registration_window, text="Пароль").pack(pady=5)
    reg_password_entry = tk.Entry(registration_window, show='*')
    reg_password_entry.pack(pady=5)

    tk.Button(registration_window, text="Зарегистрироваться", command=register_user).pack(pady=10)


# Создаем базу данных
create_database()

# Основное окно приложения
root = tk.Tk()
root.title("Авторизация")

tk.Label(root, text="Логин").pack(pady=5)
login_username_entry = tk.Entry(root)
login_username_entry.pack(pady=5)

tk.Label(root, text="Пароль").pack(pady=5)
login_password_entry = tk.Entry(root, show='*')
login_password_entry.pack(pady=5)

tk.Button(root, text="Войти", command=login_user).pack(pady=10)
tk.Button(root, text="Регистрация", command=open_registration_window).pack(pady=10)

root.mainloop()
