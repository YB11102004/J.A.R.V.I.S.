import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create the database and table if it doesn't exist
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to authenticate user
def authenticate_user():
    def verify():
        username = entry_username.get()
        password = entry_password.get()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            root.destroy()  # Close the authentication window on successful login
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def register():
        username = entry_username.get()
        password = entry_password.get()

        if username and password:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration Successful! You can now log in.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter a username and password.")

    # Create database and table
    create_database()

    # Create a Tkinter window for authentication
    root = tk.Tk()
    root.title("Authentication")
    root.geometry("550x400")
    root.configure(bg='black')  # Black background color

    # Add a title label
    title_label = tk.Label(root, text="Welcome to Jarvis!", font=("Arial", 24), bg='black', fg='white')
    title_label.pack(pady=20)

    # Create a frame for the input fields
    frame = tk.Frame(root, bg='black')
    frame.pack(pady=10)

    label_username = tk.Label(frame, text="Username:", font=("Arial", 14), bg='black', fg='white')
    label_username.grid(row=0, column=0, padx=10, pady=10)

    entry_username = tk.Entry(frame, font=("Arial", 14))
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(frame, text="Password:", font=("Arial", 14), bg='black', fg='white')
    label_password.grid(row=1, column=0, padx=10, pady=10)

    entry_password = tk.Entry(frame, show="*", font=("Arial", 14))
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    # Create a frame for buttons
    button_frame = tk.Frame(root, bg='black')
    button_frame.pack(pady=20)

    button_login = tk.Button(button_frame, text="Login", command=verify, bg='black', fg='cyan', font=("Arial", 14), width=10)
    button_login.pack(side=tk.LEFT, padx=5)

    button_register = tk.Button(button_frame, text="Register", command=register, bg='black', fg='yellow', font=("Arial", 14), width=10)
    button_register.pack(side=tk.LEFT, padx=5)

    root.mainloop()  # Start the Tkinter event loop
