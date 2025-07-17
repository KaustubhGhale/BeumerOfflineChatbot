# pages/login_page.py
import tkinter as tk
from tkinter import messagebox
from utils.theme import Theme

class LoginPage(tk.Frame):
    """
    The login page for the application.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BACKGROUND_COLOR)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Center content vertically

        # Login Frame
        login_frame = tk.Frame(self, bg=Theme.CARD_BACKGROUND_COLOR, bd=2, relief="raised", padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE)
        login_frame.grid(row=0, column=0, padx=Theme.MARGIN_LARGE, pady=Theme.MARGIN_LARGE, sticky="nsew")
        login_frame.grid_columnconfigure(0, weight=1) # Center elements within frame

        tk.Label(login_frame, text="Beumer Chatbot Login", font=(Theme.FONT_FAMILY, 20, "bold"), bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.PRIMARY_COLOR).pack(pady=20)

        # Username
        tk.Label(login_frame, text="Username:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR).pack(pady=5, anchor="w")
        self.username_entry = tk.Entry(login_frame, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), width=30, relief="solid", bd=1)
        self.username_entry.pack(pady=5, padx=Theme.PADDING_MEDIUM, fill="x")

        # Password
        tk.Label(login_frame, text="Password:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR).pack(pady=5, anchor="w")
        self.password_entry = tk.Entry(login_frame, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), show="*", width=30, relief="solid", bd=1)
        self.password_entry.pack(pady=5, padx=Theme.PADDING_MEDIUM, fill="x")

        # Login Button
        login_button = tk.Button(login_frame, text="Login", command=self._perform_login,
                                 font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM, "bold"),
                                 bg=Theme.ACCENT_COLOR, fg="white", relief="raised", bd=2,
                                 activebackground=Theme.PRIMARY_COLOR, activeforeground="white")
        login_button.pack(pady=20, padx=Theme.PADDING_MEDIUM, fill="x")

        # Bind Enter key to login
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self._perform_login())

    def _perform_login(self):
        """
        Handles the login attempt.
        For an offline app, credentials are hardcoded.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Hardcoded credentials for offline use
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Success", "Welcome to Beumer Chatbot!")
            self.controller.show_page("ChatbotPage") # Navigate to chatbot page
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            self.password_entry.delete(0, tk.END) # Clear password field

