# main.py
import tkinter as tk
from tkinter import messagebox
import os

# Custom modules
from utils.theme import Theme
from pages.login_page import LoginPage
from pages.chatbot_page import ChatbotPage
from pages.table_editor_page import TableEditorPage
from pages.about_page import AboutPage
from core.llm_handler import LLMHandler
from core.pdf_processor import PDFProcessor
from core.data_manager import DataManager

class BeumerChatbotApp(tk.Tk):
    """
    Main application class for the Beumer Offline Chatbot.
    Manages page navigation and shared resources.
    """
    def __init__(self):
        super().__init__()
        self.title("Beumer Offline Chatbot")
        self.geometry("1000x750")
        self.minsize(800, 600) # Minimum window size
        self.configure(bg=Theme.BACKGROUND_COLOR)

        # Ensure necessary directories exist
        self._create_directories()

        # Initialize shared resources
        self.llm_handler = LLMHandler()
        self.pdf_processor = PDFProcessor()
        self.data_manager = DataManager("flight_data.json") # For table editor data

        # Container for all pages
        self.container = tk.Frame(self, bg=Theme.BACKGROUND_COLOR)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._create_pages()
        self.show_page("LoginPage")

    def _create_directories(self):
        """Ensures necessary directories for models and data exist."""
        os.makedirs("models", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        print("Ensured 'models' and 'data' directories exist.")

    def _create_pages(self):
        """Initializes and stores all application pages."""
        for PageClass in (LoginPage, ChatbotPage, TableEditorPage, AboutPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name: str):
        """
        Raises a specific page to the top, making it visible.
        """
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
            print(f"Showing page: {page_name}")
        else:
            messagebox.showerror("Navigation Error", f"Page '{page_name}' not found.")

    def logout(self):
        """Handles logout functionality, returning to the login page."""
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.show_page("LoginPage")
            messagebox.showinfo("Logged Out", "You have been logged out.")

if __name__ == "__main__":
    app = BeumerChatbotApp()
    app.mainloop()

