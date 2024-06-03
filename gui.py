import tkinter as tk
from tkinter import messagebox
from client import Client

class GUI:
    def __init__(self, host, port):
        self.client = Client(host, port)
        self.window = tk.Tk()
        self.window.title("PyChat")

        # Create login and registration frames
        self.login_frame = tk.Frame(self.window)
        self.register_frame = tk.Frame(self.window)

        # Create login widgets
        tk.Label(self.login_frame, text="Username:").pack()
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack()
        tk.Label(self.login_frame, text="Password:").pack()
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack()
        tk.Button(self.login_frame, text="Login", command=self.login).pack()
        tk.Button(self.login_frame, text="Register", command=self.show_register_frame).pack()

        # Create registration widgets
        tk.Label(self.register_frame, text="Username:").pack()
        self.register_username_entry = tk.Entry(self.register_frame)
        self.register_username_entry.pack()
        tk.Label(self.register_frame, text="Password:").pack()
        self.register_password_entry = tk.Entry(self.register_frame, show="*")
        self.register_password_entry.pack()
        tk.Button(self.register_frame, text="Register", command=self.register).pack()
        tk.Button(self.register_frame, text="Back to Login", command=self.show_login_frame).pack()

        # Create chat frame
        self.chat_frame = tk.Frame(self.window)
        self.chat_history = tk.Text(self.chat_frame, height=20, width=50)
        self.chat_history.pack()

        self.message_entry = tk.Entry(self.chat_frame, width=50)
        self.message_entry.pack()

        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack()

        # Create user list frame
        self.user_list_frame = tk.Frame(self.window)
        self.user_list = tk.Listbox(self.user_list_frame)
        self.user_list.pack()

    def start(self):
        self.client.set_message_callback(self.display_message)
        self.client.connect()
        self.show_login_frame()
        self.window.mainloop()

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.chat_frame.pack_forget()
        self.user_list_frame.pack_forget()
        self.login_frame.pack()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.chat_frame.pack_forget()
        self.user_list_frame.pack_forget()
        self.register_frame.pack()

    def show_chat_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack_forget()
        self.chat_frame.pack(side=tk.LEFT)
        self.user_list_frame.pack(side=tk.RIGHT)

    def login(self):
      username = self.login_username_entry.get()
      password = self.login_password_entry.get()
      login_message = f"/login {username} {password}"
      self.client.send_message(login_message)
      response = self.client.client_socket.recv(1024).decode()
      if response == "Login successful":
          self.client.username = username
          self.show_chat_frame()
      else:
          messagebox.showerror("Login Failed", response)

    def register(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        register_message = f"/register {username} {password}"
        self.client.send_message(register_message)
        response = self.client.client_socket.recv(1024).decode()
        if response == "Registration successful":
            messagebox.showinfo("Registration", response)
            self.show_login_frame()
        else:
            messagebox.showerror("Registration Failed", response)

    def send_message(self):
        message = self.message_entry.get()
        self.client.send_message(message)
        self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.see(tk.END)