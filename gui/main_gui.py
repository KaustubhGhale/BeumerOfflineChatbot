import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os
from chatbot.chatbot import PDFChatbot
from table.crud_table import CrudTable
from database.db import insert_pdf_data, insert_flight
from utils.pdf_parser import extract_text_from_pdf
import re

class ChatbotPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.chatbot = PDFChatbot()

        tk.Button(self, text="Upload PDF", command=self.upload_pdf).pack(pady=10)

        self.chat_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=20, width=80)
        self.chat_area.pack(padx=10, pady=10)

        self.user_input = tk.Entry(self, width=80)
        self.user_input.pack(pady=5)

        tk.Button(self, text="Ask", command=self.ask_question).pack(pady=5)
        tk.Button(self, text="Go to Table View", command=lambda: controller.show_frame("TablePage")).pack(pady=10)

    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            text, tables = extract_text_from_pdf(file_path)

            if not text:
                messagebox.showerror("Error", "Failed to extract any content from PDF.")
                return

            # Save the raw text in the database
            insert_pdf_data(os.path.basename(file_path), text)

            # Attempt to find and insert flight table data
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

            messagebox.showinfo("Success", f"PDF uploaded successfully.\n")

    def ask_question(self):
        question = self.user_input.get()
        if question:
            response = self.chatbot.ask(question)
            self.chat_area.insert(tk.END, f"You: {question}\nBot: {response}\n\n")
            self.user_input.delete(0, tk.END)

class TablePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.table = CrudTable(self)
        self.table.pack()

        tk.Button(self, text="Go to Chatbot View", command=lambda: controller.show_frame("ChatbotPage")).pack(pady=10)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline Chatbot with Table")
        self.geometry("900x700")

        container = tk.Frame(self)
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
    from database.db import init_db
    init_db()
    app = App()
    app.mainloop()
