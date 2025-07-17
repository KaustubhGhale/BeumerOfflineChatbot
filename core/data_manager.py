# core/data_manager.py
import json
import os

class DataManager:
    """
    Handles saving and loading of structured data (e.g., table data) to/from a JSON file.
    """
    def __init__(self, filename: str = "app_data.json"):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True) # Ensure data directory exists
        self.filepath = os.path.join(self.data_dir, filename)
        print(f"Data Manager initialized. Data will be stored at: {self.filepath}")

    def save_data(self, data: list):
        """
        Saves a list of dictionaries (e.g., table rows) to the JSON file.
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"Data successfully saved to {self.filepath}")
        except Exception as e:
            print(f"Error saving data to {self.filepath}: {e}")
            raise RuntimeError(f"Failed to save data: {e}") from e

    def load_data(self) -> list:
        """
        Loads data from the JSON file. Returns an empty list if file doesn't exist.
        """
        if not os.path.exists(self.filepath):
            print(f"Data file not found at {self.filepath}. Returning empty list.")
            return []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Data successfully loaded from {self.filepath}")
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.filepath}: {e}. File might be corrupted or empty.")
            # Optionally, back up the corrupted file and return empty data
            return []
        except Exception as e:
            print(f"Error loading data from {self.filepath}: {e}")
            raise RuntimeError(f"Failed to load data: {e}") from e

