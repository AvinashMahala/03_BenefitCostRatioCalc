import tkinter as tk
from tkinter import messagebox

def validate_total_quantity(value):
    if value == "":
        return True  # Allow empty input
    try:
        quantity = int(value)
        if 0 <= quantity <= 10000:
            return True
        else:
            messagebox.showerror("Error", "Quantity must be between 0 and 10000.")
            return False
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")
        return False
