# pages/table_editor_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.theme import Theme
import pandas as pd

class TableEditorPage(tk.Frame):
    """
    Page for viewing and manually editing tabular data.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=Theme.BACKGROUND_COLOR)
        self.controller = controller
        self.table_data = pd.DataFrame(columns=["Serial No", "Flight Name", "Destination", "IATA"]) # Initialize empty DataFrame

        self._create_widgets()
        self._load_data() # Load existing data on page creation

    def _create_widgets(self):
        """
        Creates all the GUI widgets for the table editor page.
        """
        # --- Navigation Bar ---
        nav_frame = tk.Frame(self, bg=Theme.PRIMARY_COLOR, height=50)
        nav_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        tk.Label(nav_frame, text="Flight Table Editor", font=(Theme.FONT_FAMILY, 16, "bold"), bg=Theme.PRIMARY_COLOR, fg="white").pack(side=tk.LEFT, padx=Theme.PADDING_MEDIUM)

        # Navigation Buttons
        nav_buttons_frame = tk.Frame(nav_frame, bg=Theme.PRIMARY_COLOR)
        nav_buttons_frame.pack(side=tk.RIGHT, padx=Theme.PADDING_MEDIUM)

        tk.Button(nav_buttons_frame, text="Chatbot", command=lambda: self.controller.show_page("ChatbotPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="About Us", command=lambda: self.controller.show_page("AboutPage"),
                  bg=Theme.ACCENT_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_buttons_frame, text="Logout", command=self.controller.logout,
                  bg=Theme.ERROR_COLOR, fg="white", relief="flat", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM)).pack(side=tk.LEFT, padx=5)

        # --- Table Display Area ---
        table_frame = tk.Frame(self, bg=Theme.CARD_BACKGROUND_COLOR, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM, bd=2, relief="sunken")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=Theme.MARGIN_MEDIUM, pady=Theme.MARGIN_MEDIUM)

        # Create Treeview (Table)
        self.tree = ttk.Treeview(table_frame, columns=list(self.table_data.columns), show="headings")
        for col in self.table_data.columns:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=150, anchor="w") # Default width
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=hsb.set)

        # --- Input for New Entry ---
        input_frame = tk.Frame(self, bg=Theme.CARD_BACKGROUND_COLOR, padx=Theme.PADDING_MEDIUM, pady=Theme.PADDING_MEDIUM, bd=2, relief="ridge")
        input_frame.pack(fill=tk.X, expand=False, padx=Theme.MARGIN_MEDIUM, pady=Theme.MARGIN_MEDIUM)

        self.entries = {}
        for i, col in enumerate(self.table_data.columns):
            tk.Label(input_frame, text=f"{col}:", bg=Theme.CARD_BACKGROUND_COLOR, fg=Theme.TEXT_COLOR, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL)).grid(row=0, column=i, padx=5, pady=2, sticky="w")
            entry = tk.Entry(input_frame, width=20, relief="solid", bd=1, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL))
            entry.grid(row=1, column=i, padx=5, pady=2, sticky="ew")
            self.entries[col] = entry
            input_frame.grid_columnconfigure(i, weight=1) # Make columns expand

        self.add_button = tk.Button(input_frame, text="Add Row", command=self._add_row,
                                     bg=Theme.ACCENT_COLOR, fg="white", relief="raised", bd=2,
                                     activebackground=Theme.PRIMARY_COLOR, activeforeground="white",
                                     font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM))
        self.add_button.grid(row=1, column=len(self.table_data.columns), padx=5, pady=2)

        self.delete_button = tk.Button(input_frame, text="Delete Selected", command=self._delete_selected_row,
                                       bg=Theme.ERROR_COLOR, fg="white", relief="raised", bd=2,
                                       activebackground=Theme.PRIMARY_COLOR, activeforeground="white",
                                       font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_MEDIUM))
        self.delete_button.grid(row=2, column=0, columnspan=len(self.table_data.columns) + 1, pady=10)

        # Status bar for table editor
        self.status_bar = tk.Label(self, text="Ready.", bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL), bg=Theme.BACKGROUND_COLOR, fg=Theme.TEXT_COLOR)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_data(self):
        """Loads data from the DataManager and populates the Treeview."""
        try:
            loaded_data = self.controller.data_manager.load_data()
            if loaded_data:
                # Assuming loaded_data is a list of dicts, convert to DataFrame
                self.table_data = pd.DataFrame(loaded_data)
                # Ensure all expected columns exist, add if missing
                for col in ["Serial No", "Flight Name", "Destination", "IATA"]:
                    if col not in self.table_data.columns:
                        self.table_data[col] = "" # Add missing column with empty values
                self.table_data = self.table_data[self.tree["columns"]] # Reorder columns if needed
            else:
                self.table_data = pd.DataFrame(columns=["Serial No", "Flight Name", "Destination", "IATA"]) # Reset if no data

            self._populate_treeview()
            self.update_status("Table data loaded.", Theme.SUCCESS_COLOR)
        except Exception as e:
            self.update_status(f"Error loading table data: {e}", Theme.ERROR_COLOR)
            messagebox.showerror("Load Error", f"Error loading table data: {e}")

    def _populate_treeview(self):
        """Clears and repopulates the Treeview with current table_data."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, row in self.table_data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def _add_row(self):
        """Adds a new row to the table from input fields."""
        new_row_data = {col: self.entries[col].get().strip() for col in self.table_data.columns}

        # Basic validation: ensure at least Flight Name is not empty
        if not new_row_data["Flight Name"]:
            self.update_status("Flight Name cannot be empty.", Theme.ERROR_COLOR)
            messagebox.showwarning("Input Error", "Flight Name cannot be empty.")
            return

        # Append new row to DataFrame
        self.table_data = pd.concat([self.table_data, pd.DataFrame([new_row_data])], ignore_index=True)
        self._populate_treeview()
        self._save_data()
        self.update_status("Row added successfully.", Theme.SUCCESS_COLOR)
        for entry in self.entries.values():
            entry.delete(0, tk.END) # Clear input fields

    def _delete_selected_row(self):
        """Deletes the selected row(s) from the table."""
        selected_items = self.tree.selection()
        if not selected_items:
            self.update_status("No row selected for deletion.", Theme.ERROR_COLOR)
            messagebox.showwarning("Delete Error", "Please select a row to delete.")
            return

        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected row(s)?"):
            indices_to_delete = []
            for item in selected_items:
                # Get the values of the selected row
                values = self.tree.item(item, 'values')
                # Find the index in the DataFrame that matches these values
                # This assumes values are unique enough to identify a row,
                # or you might need a hidden ID column for robust deletion.
                # For simplicity, we'll try to match all values.
                try:
                    # Convert values to a list for comparison with Series
                    row_list = list(values)
                    # Find index where all column values match
                    idx = self.table_data.index[(self.table_data.eq(row_list).all(axis=1))].tolist()
                    if idx:
                        indices_to_delete.extend(idx)
                except Exception as e:
                    print(f"Error finding index for deletion: {e}")
                    continue

            if indices_to_delete:
                # Drop rows from DataFrame based on found indices
                self.table_data = self.table_data.drop(index=indices_to_delete).reset_index(drop=True)
                self._populate_treeview()
                self._save_data()
                self.update_status("Row(s) deleted successfully.", Theme.SUCCESS_COLOR)
            else:
                self.update_status("Could not find matching row(s) to delete.", Theme.ERROR_COLOR)
                messagebox.showerror("Deletion Error", "Could not find matching row(s) in data to delete.")

    def _save_data(self):
        """Saves the current table data using the DataManager."""
        try:
            # Convert DataFrame to list of dictionaries for JSON serialization
            data_to_save = self.table_data.to_dict(orient='records')
            self.controller.data_manager.save_data(data_to_save)
            self.update_status("Table data saved.", Theme.SUCCESS_COLOR)
        except Exception as e:
            self.update_status(f"Error saving table data: {e}", Theme.ERROR_COLOR)
            messagebox.showerror("Save Error", f"Error saving table data: {e}")

    def update_status(self, message: str, color: str = Theme.TEXT_COLOR):
        """
        Updates the status bar with a given message and color.
        """
        self.status_bar.config(text=message, fg=color)
        self.controller.update_idletasks() # Ensure UI updates immediately

