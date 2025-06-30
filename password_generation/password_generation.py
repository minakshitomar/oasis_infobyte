import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# Generate secure password
def generate_password():
    try:
        length = int(length_var.get())
        if length < 4:
            raise ValueError("Password must be at least 4 characters")

        use_upper = upper_var.get()
        use_lower = lower_var.get()
        use_digits = digits_var.get()
        use_symbols = symbols_var.get()
        exclude_chars = exclude_var.get()

        if not any([use_upper, use_lower, use_digits, use_symbols]):
            messagebox.showerror("Error", "Select at least one character type.")
            return

        char_sets = []
        password = []

        if use_upper:
            char_sets.append(string.ascii_uppercase)
            password.append(random.choice(string.ascii_uppercase))
        if use_lower:
            char_sets.append(string.ascii_lowercase)
            password.append(random.choice(string.ascii_lowercase))
        if use_digits:
            char_sets.append(string.digits)
            password.append(random.choice(string.digits))
        if use_symbols:
            char_sets.append(string.punctuation)
            password.append(random.choice(string.punctuation))

        # Combine and remove excluded characters
        all_chars = ''.join(char_sets)
        if exclude_chars:
            all_chars = ''.join(c for c in all_chars if c not in exclude_chars)

        if len(all_chars) == 0:
            messagebox.showerror("Error", "Character set is empty after exclusions.")
            return

        while len(password) < length:
            password.append(random.choice(all_chars))

        random.shuffle(password)
        final_password = ''.join(password[:length])
        password_entry.delete(0, tk.END)
        password_entry.insert(0, final_password)

    except ValueError as ve:
        messagebox.showerror("Invalid Input", str(ve))

# Copy to clipboard
def copy_password():
    pwd = password_entry.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# Tkinter window
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x420")
root.resizable(False, False)

tk.Label(root, text="Password Length:").pack(pady=5)
length_var = tk.StringVar()
length_entry = tk.Entry(root, textvariable=length_var)
length_entry.pack(pady=5)
length_var.set("12")

# Options
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Include Uppercase Letters (A-Z)", variable=upper_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Lowercase Letters (a-z)", variable=lower_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Digits (0-9)", variable=digits_var).pack(anchor='w', padx=20)
tk.Checkbutton(root, text="Include Symbols (!@#$)", variable=symbols_var).pack(anchor='w', padx=20)

tk.Label(root, text="Exclude Characters (e.g. oO0l1):").pack(pady=5)
exclude_var = tk.StringVar()
exclude_entry = tk.Entry(root, textvariable=exclude_var)
exclude_entry.pack(pady=5)

# Generated password display
tk.Label(root, text="Generated Password:").pack(pady=5)
password_entry = tk.Entry(root, font=('Courier', 12), justify='center')
password_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Generate Password", command=generate_password, bg="lightblue").pack(pady=10)
tk.Button(root, text="Copy to Clipboard", command=copy_password, bg="lightgreen").pack(pady=5)

root.mainloop()
