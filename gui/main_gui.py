import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Entry, Button, Frame, Label

from chatbot.chatbot import PDFChatbot
from table.crud_table import CrudTable
from database.db import insert_pdf_data, insert_flight, init_db
from utils.pdf_parser import extract_text_from_pdf


class ChatbotPage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller
        self.chatbot = PDFChatbot()

        Label(self, text="Offline Chatbot", font=("Helvetica", 16, "bold")).pack(pady=10)

        Button(self, text="Upload PDF", bootstyle=PRIMARY, command=self.upload_pdf).pack(pady=5)

        self.chat_area = ScrolledText(self, wrap=tk.WORD, height=20, width=100)
        self.chat_area.pack(pady=10)

        entry_frame = Frame(self)
        entry_frame.pack(fill=X, pady=5)

        self.user_input = Entry(entry_frame, width=80)
        self.user_input.pack(side=LEFT, padx=(0, 10), fill=X, expand=True)
        self.user_input.bind("<Return>", lambda event: self.ask_question())

        Button(entry_frame, text="Ask", bootstyle=SUCCESS, command=self.ask_question).pack(side=LEFT)

        Button(self, text="Clear Chat", bootstyle=SECONDARY, command=self.clear_chat).pack(pady=5)
        Button(self, text="Go to Table View", bootstyle=INFO, command=lambda: controller.show_frame("TablePage")).pack(pady=10)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            text, tables = extract_text_from_pdf(file_path)

            if not text:
                messagebox.showerror("Error", "Failed to extract any content from PDF.")
                return

            insert_pdf_data(os.path.basename(file_path), text)

            inserted = False
            for table in tables:
                if table and isinstance(table, list):
                    headers = [h.lower().strip() for h in table[0] if h]
                    try:
                        s_idx = headers.index("serial no")
                        f_idx = headers.index("flight name")
                        d_idx = headers.index("destination")
                        i_idx = headers.index("iata")

                        for row in table[1:]:
                            if len(row) >= max(s_idx, f_idx, d_idx, i_idx) + 1:
                                serial_no = row[s_idx].strip()
                                flight_name = row[f_idx].strip()
                                destination = row[d_idx].strip()
                                iata = row[i_idx].strip()
                                if serial_no and flight_name:
                                    insert_flight(serial_no, flight_name, destination, iata)
                                    inserted = True
                    except ValueError:
                        continue

            messagebox.showinfo("Success", "PDF uploaded and processed successfully.")

    def ask_question(self):
        question = self.user_input.get()
        if not question.strip():
            return
        self.chat_area.insert(tk.END, f"You: {question}\n")
        self.chat_area.insert(tk.END, "Bot is typing...\n")
        self.chat_area.see(tk.END)
        self.user_input.delete(0, tk.END)

        def get_response():
            response = self.chatbot.ask(question)
            self.chat_area.delete("end-2l", "end-1l")  # Remove "Bot is typing..."
            self.typing_animation(f"Bot: {response}\n\n")

        threading.Thread(target=get_response).start()

    def typing_animation(self, text):
        for char in text:
            self.chat_area.insert(tk.END, char)
            self.chat_area.see(tk.END)
            self.chat_area.update()
            self.chat_area.after(10)

    def clear_chat(self):
        self.chat_area.delete(1.0, tk.END)


class TablePage(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=10)
        self.controller = controller

        Label(self, text="Flight Table View", font=("Helvetica", 16, "bold")).pack(pady=10)
        self.table = CrudTable(self)
        self.table.pack(pady=10)

        Button(self, text="Go to Chatbot View", bootstyle=INFO, command=lambda: controller.show_frame("ChatbotPage")).pack(pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline AI Chatbot System")
        self.geometry("1000x750")
        self.style = Style("flatly")

        container = Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (ChatbotPage, TablePage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ChatbotPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    init_db()
    app = App()
    app.mainloop()
