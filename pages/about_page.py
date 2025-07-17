# pages/about_page.py
import tkinter as tk
from utils.theme import Theme

class AboutPage(tk.Frame):
    """
    The About Us page for the application.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BACKGROUND_COLOR)
        self.controller = controller

        self._create_widgets()

    def _create_widgets(self):
        """
        Creates all the GUI widgets for the about page.
        """
        # --- Navigation Bar ---
        nav_frame = tk.Frame(self, bg=Theme.PRIMARY_COLOR, height=50)
        nav_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        tk.Label(nav_frame, text="About Beumer Chatbot", font=(Theme.FONT_FAMILY, 16, "bold"), bg=Theme.PRIMARY_COLOR, fg="white").pack(side=tk.LEFT, padx=Theme.PADDING_MEDIUM)

        # Navigation Buttons
        nav_buttons_frame = tk.Frame(nav_frame, bg=Theme.PRIMARY_COLOR)
        nav_buttons_frame.pack(side=tk.RIGHT, padx=Theme.PADDING_MEDIUM)

        tk.Button(nav_buttons_frame, text="Chatbot", command=lambda: self.controller.show_page("ChatbotPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="Table Editor", command=lambda: self.controller.show_page("TableEditorPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="Logout", command=self.controller.logout,
                  bg=Theme.ERROR_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)

        # --- Content Area ---
        content_frame = tk.Frame(self, bg=Theme.CARD_BACKGROUND_COLOR, padx=Theme.PADDING_LARGE, pady=Theme.PADDING_LARGE, bd=2, relief="groove")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.MARGIN_LARGE, pady=Theme.MARGIN_LARGE)

        tk.Label(content_frame, text="About Beumer Offline Chatbot",
                 font=(Theme.FONT_FAMILY, 18, "bold"), bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.PRIMARY_COLOR).pack(pady=10)

        about_text = """
This Beumer Offline Chatbot is designed to provide quick and accurate information
from airport-related PDF documents, such as baggage handling systems, pipelines,
and flight details. It leverages a local Large Language Model (LLM) to understand
your queries and retrieve relevant information from the processed documents.

Key Features:
- Offline operation: No internet connection required after initial setup.
- Document-based Q&A: Ask questions about uploaded PDFs.
- Local LLM: Utilizes powerful open-source language models for intelligent responses.
- Manual Table Editor: Manage structured data like flight details directly within the app.
- Intuitive User Interface: Designed with Beumer's brand aesthetics in mind.

Developed as a proof-of-concept for internal use at Beumer.

Version: 1.0.0
Developed by: Kaustubh Ghale
For: Beumer Internship Project
"""
        tk.Label(content_frame, text=about_text, justify=tk.LEFT, wraplength=700,
                 font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR).pack(pady=10, fill="x")

