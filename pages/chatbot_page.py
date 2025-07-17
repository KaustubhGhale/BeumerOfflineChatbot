# pages/chatbot_page.py
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import os
from utils.theme import Theme

class ChatbotPage(tk.Frame):
    """
    The main chatbot interface page.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BACKGROUND_COLOR)
        self.controller = controller

        self.document_path = None
        self.model_path = None

        self._create_widgets()
        self.update_status("Welcome! Please load a PDF document and the LLM model.", Theme.INFO_COLOR)
        self.set_ui_state(False) # Initially disable chat input

    def _create_widgets(self):
        """
        Creates all the GUI widgets for the chatbot page.
        """
        # --- Navigation Bar ---
        nav_frame = tk.Frame(self, bg=Theme.PRIMARY_COLOR, height=50)
        nav_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        tk.Label(nav_frame, text="Beumer Chatbot", font=(Theme.FONT_FAMILY, 16, "bold"), bg=Theme.PRIMARY_COLOR, fg="white").pack(side=tk.LEFT, padx=Theme.PADDING_MEDIUM)

        # Navigation Buttons
        nav_buttons_frame = tk.Frame(nav_frame, bg=Theme.PRIMARY_COLOR)
        nav_buttons_frame.pack(side=tk.RIGHT, padx=Theme.PADDING_MEDIUM)

        tk.Button(nav_buttons_frame, text="Table Editor", command=lambda: self.controller.show_page("TableEditorPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="About Us", command=lambda: self.controller.show_page("AboutPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="Logout", command=self.controller.logout,
                  bg=Theme.ERROR_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)


        # --- Top Frame for File Selection ---
        top_frame = tk.Frame(self, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM, bg=Theme.CARD_BACKGROUND_COLOR, bd=2, relief="groove")
        top_frame.pack(side=tk.TOP, fill=tk.X, expand=False, padx=Theme.MARGIN_MEDIUM, pady=Theme.MARGIN_MEDIUM)

        # PDF Selection
        tk.Label(top_frame, text="PDF Document:", bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL)).grid(row=0, column=0, sticky="w", pady=2)
        self.pdf_entry = tk.Entry(top_frame, width=50, state="readonly", relief="solid", bd=1, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL))
        self.pdf_entry.grid(row=0, column=1, padx=5, pady=2)
        self.pdf_button = tk.Button(top_frame, text="Browse PDF", command=self._load_pdf_document,
                                     bg=Theme.ACCENT_COLOR, fg="white", relief="raised", bd=2,
                                     activebackground=Theme.PRIMARY_COLOR, activeforeground="white",
                                     font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL))
        self.pdf_button.grid(row=0, column=2, padx=5, pady=2)

        # Model Selection
        tk.Label(top_frame, text="LLM Model (.gguf):", bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL)).grid(row=1, column=0, sticky="w", pady=2)
        self.model_entry = tk.Entry(top_frame, width=50, state="readonly", relief="solid", bd=1, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL))
        self.model_entry.grid(row=1, column=1, padx=5, pady=2)
        self.model_button = tk.Button(top_frame, text="Browse Model", command=self._load_llm_model,
                                       bg=Theme.ACCENT_COLOR, fg="white", relief="raised", bd=2,
                                       activebackground=Theme.PRIMARY_COLOR, activeforeground="white",
                                       font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL))
        self.model_button.grid(row=1, column=2, padx=5, pady=2)

        # Initialize Chatbot Button
        self.init_chatbot_button = tk.Button(top_frame, text="Initialize Chatbot", command=self._initialize_chatbot_thread,
                                             bg=Theme.PRIMARY_COLOR, fg="white", relief="raised", bd=2,
                                             activebackground=Theme.ACCENT_COLOR, activeforeground="white",
                                             font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM, "bold"))
        self.init_chatbot_button.grid(row=2, column=0, columnspan=3, pady=10)

        # --- Chat Display Area ---
        chat_frame = tk.Frame(self, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM, bg=Theme.CARD_BACKGROUND_COLOR, bd=2, relief="sunken")
        chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=Theme.MARGIN_MEDIUM, pady=Theme.MARGIN_MEDIUM)

        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state="disabled",
                                                      font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM),
                                                      bg="#ffffff", fg=Theme.TEXT_COLOR, relief="flat", bd=0)
        self.chat_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.chat_display.tag_config("User", foreground=Theme.ACCENT_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM, "bold"))
        self.chat_display.tag_config("Bot", foreground=Theme.SUCCESS_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM, "bold"))
        self.chat_display.tag_config("normal", foreground=Theme.TEXT_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM))


        # --- Input Area ---
        input_frame = tk.Frame(self, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM, bg=Theme.CARD_BACKGROUND_COLOR, bd=2, relief="ridge")
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=False, padx=Theme.MARGIN_MEDIUM, pady=Theme.MARGIN_MEDIUM)

        self.user_input = tk.Entry(input_frame, width=70, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM), relief="solid", bd=1)
        self.user_input.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self._send_message_event) # Bind Enter key

        self.send_button = tk.Button(input_frame, text="Send", command=self._send_message,
                                     bg=Theme.ACCENT_COLOR, fg="white", relief="raised", bd=2,
                                     activebackground=Theme.PRIMARY_COLOR, activeforeground="white",
                                     font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM))
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # --- Status Bar ---
        self.status_bar = tk.Label(self, text="Ready.", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL), bg=Theme.BACKGROUND_COLOR, fg=Theme.TEXT_COLOR)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_ui_state(self, chatbot_ready: bool):
        """
        Enables or disables UI elements based on chatbot readiness.
        """
        state = "normal" if chatbot_ready else "disabled"
        self.user_input.config(state=state)
        self.send_button.config(state=state)
        self.init_chatbot_button.config(state="normal" if not chatbot_ready else "disabled")
        self.pdf_button.config(state="normal" if not chatbot_ready else "disabled")
        self.model_button.config(state="normal" if not chatbot_ready else "disabled")

    def update_status(self, message: str, color: str = Theme.TEXT_COLOR):
        """
        Updates the status bar with a given message and color.
        """
        self.status_bar.config(text=message, fg=color)
        self.controller.update_idletasks() # Ensure UI updates immediately

    def display_message(self, sender: str, message: str, tag: str = "normal"):
        """
        Displays a message in the chat display area.
        """
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", "normal")
        self.chat_display.yview(tk.END)
        self.chat_display.config(state="disabled")

    def _load_pdf_document(self):
        """
        Opens a file dialog to select a PDF document.
        """
        filepath = filedialog.askopenfilename(
            title="Select PDF Document",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filepath:
            self.document_path = filepath
            self.pdf_entry.config(state="normal")
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, os.path.basename(filepath))
            self.pdf_entry.config(state="readonly")
            self.update_status(f"PDF selected: {os.path.basename(filepath)}", Theme.INFO_COLOR)
        else:
            self.update_status("PDF selection cancelled.", Theme.ERROR_COLOR)

    def _load_llm_model(self):
        """
        Opens a file dialog to select the LLM model file (.gguf).
        """
        filepath = filedialog.askopenfilename(
            title="Select LLM Model (.gguf)",
            filetypes=[("GGUF models", "*.gguf")],
            initialdir=os.path.join(os.getcwd(), "models") # Start in models folder
        )
        if filepath:
            self.model_path = filepath
            self.model_entry.config(state="normal")
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, os.path.basename(filepath))
            self.model_entry.config(state="readonly")
            self.update_status(f"Model selected: {os.path.basename(filepath)}", Theme.INFO_COLOR)
        else:
            self.update_status("Model selection cancelled.", Theme.ERROR_COLOR)

    def _initialize_chatbot_thread(self):
        """
        Initializes the chatbot in a separate thread to prevent GUI freezing.
        """
        if not self.document_path:
            messagebox.showerror("Error", "Please select a PDF document first.")
            return
        if not self.model_path:
            messagebox.showerror("Error", "Please select the LLM model file first.")
            return

        self.set_ui_state(False) # Disable UI during initialization
        self.update_status("Initializing chatbot... This may take a while.", Theme.INFO_COLOR)
        threading.Thread(target=self._initialize_chatbot_task, daemon=True).start()

    def _initialize_chatbot_task(self):
        """
        The actual chatbot initialization task run in a separate thread.
        """
        try:
            # 1. Process PDF
            self.update_status("Extracting text from PDF...", Theme.INFO_COLOR)
            document_text = self.controller.pdf_processor.extract_text_from_pdf(self.document_path)
            self.update_status("Creating document embeddings...", Theme.INFO_COLOR)
            self.controller.pdf_processor.create_embeddings(document_text)

            # 2. Load LLM
            self.update_status("Loading LLM model... (This is memory intensive)", Theme.INFO_COLOR)
            # Configure LLM for CPU-only for maximum compatibility on new AMD chips
            llm_config = {
                'n_ctx': 4096, # Context window size
                'n_batch': 512, # Batch size for prompt processing
                'n_threads': os.cpu_count(), # Use all available CPU threads
                'n_gpu_layers': 0, # Force CPU-only to avoid GPU compatibility issues
                'verbose': True # Enable verbose output from llama.cpp
            }
            self.controller.llm_handler.load_model(self.model_path, llm_config)

            self.master.after(0, lambda: self.update_status("Chatbot ready! You can now ask questions.", Theme.SUCCESS_COLOR))
            self.master.after(0, lambda: self.set_ui_state(True))
        except Exception as e:
            error_message = f"Failed to initialize chatbot: {e}"
            print(f"Initialization Error: {e}") # Print to console for debugging
            self.master.after(0, lambda: self.update_status(error_message, Theme.ERROR_COLOR))
            self.master.after(0, lambda: messagebox.showerror("Initialization Error", error_message))
            self.master.after(0, lambda: self.set_ui_state(False)) # Re-enable file selection, disable chat

    def _send_message_event(self, event=None):
        """
        Handles sending message when Enter key is pressed.
        """
        self._send_message()

    def _send_message(self):
        """
        Sends the user's message to the chatbot and displays the response.
        """
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        self.display_message("User", user_text, "User")
        self.user_input.delete(0, tk.END) # Clear input box immediately
        self.set_ui_state(False) # Disable input while bot is typing
        self.update_status("Bot is typing...", Theme.INFO_COLOR)

        # Run chatbot inference in a separate thread
        threading.Thread(target=self._get_chatbot_response_task, args=(user_text,), daemon=True).start()

    def _get_chatbot_response_task(self, user_text: str):
        """
        The actual chatbot response generation task run in a separate thread.
        """
        try:
            response = self.controller.llm_handler.get_response(user_text)
            self.master.after(0, lambda: self.display_message("Bot", response, "Bot"))
        except Exception as e:
            error_message = f"Error generating response: {e}"
            print(f"Response Generation Error: {e}") # Print to console for debugging
            self.master.after(0, lambda: self.display_message("Bot", f"An error occurred: {e}", "normal"))
            self.master.after(0, lambda: self.update_status(error_message, Theme.ERROR_COLOR))
            self.master.after(0, lambda: messagebox.showerror("Chatbot Error", error_message))
        finally:
            self.master.after(0, lambda: self.update_status("Ready for your next question.", Theme.SUCCESS_COLOR))
            self.master.after(0, lambda: self.set_ui_state(True)) # Re-enable input

