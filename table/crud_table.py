import tkinter as tk
from tkinter import ttk, messagebox
from database.db import insert_flight, flight_exists, update_flight, delete_flight, get_all_flights

class CrudTable(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, columns=("Serial No", "Flight Name", "Destination", "IATA"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10)

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=10)

        self.entries = {}
        self.fields = ["Serial No", "Flight Name", "Destination", "IATA"]
        for idx, field in enumerate(self.fields):
            tk.Label(self.input_frame, text=field).grid(row=0, column=idx)
            entry = tk.Entry(self.input_frame)
            entry.grid(row=1, column=idx)
            self.entries[field] = entry

        tk.Button(self.input_frame, text="Send", command=self.add_row).grid(row=1, column=len(self.fields), padx=10)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_row)
        self.context_menu.add_command(label="Delete", command=self.delete_row)

        self.load_data()

    def add_row(self):
        values = [self.entries[field].get().strip() for field in self.fields]
        if not all(values):
            messagebox.showwarning("Input Error", "Please fill all fields before sending.")
            return

        serial_no, flight_name, destination, iata = values
        if flight_exists(serial_no, flight_name, destination, iata):
            messagebox.showerror("Duplicate Entry", "One or more fields already exist.")
            return

        insert_flight(serial_no, flight_name, destination, iata)
        self.tree.insert("", "end", values=values)
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def load_data(self):
        for row in get_all_flights():
            self.tree.insert("", "end", values=row)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_row(self):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])['values']
        delete_flight(*values)
        self.tree.delete(selected[0])

    def edit_row(self):
        selected = self.tree.selection()
        if not selected:
            return
        old_values = self.tree.item(selected[0])['values']
        new_values = [self.entries[field].get().strip() for field in self.fields]
        if not all(new_values):
            messagebox.showwarning("Input Error", "Fill all fields before editing.")
            return

        update_flight(old_values, new_values)
        self.tree.item(selected[0], values=new_values)
        for entry in self.entries.values():
            entry.delete(0, tk.END)
