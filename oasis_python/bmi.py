import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def setup_database():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY,
            name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_record(name, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bmi_records (name, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, weight, height, bmi, category))
    conn.commit()
    conn.close()

def fetch_records():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bmi_records')
    records = cursor.fetchall()
    conn.close()
    return records

def plot_bmi_trends():
    records = fetch_records()
    if not records:
        messagebox.showinfo("No Data", "No BMI records found.")
        return

    names = [record[1] for record in records]
    bmis = [record[4] for record in records]

    plt.figure(figsize=(10, 5))
    plt.bar(names, bmis, color='skyblue')
    plt.xlabel('Names')
    plt.ylabel('BMI')
    plt.title('BMI Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def calculate_bmi():
    try:
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return
        
        bmi = weight / (height ** 2)
        category = classify_bmi(bmi)
        
        result_label.config(text=f"{name}, your BMI is: {bmi:.2f}\nCategory: {category}")
        save_record(name, weight, height, bmi, category)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def classify_bmi(bmi):
    """Classify BMI into categories"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# Create the main window
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Setup database
setup_database()

# Create and place the labels and entry fields with padding
tk.Label(root, text="Name:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg):", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
weight_entry = tk.Entry(root, font=("Arial", 12))
weight_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m):", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
height_entry = tk.Entry(root, font=("Arial", 12))
height_entry.grid(row=2, column=1, padx=10, pady=10)

# Create and place the calculate button
calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi, bg="#4CAF50", fg="white", font=("Arial", 12))
calculate_button.grid(row=3, columnspan=2, pady=20)

# Create and place the plot button
plot_button = tk.Button(root, text="View BMI Trends", command=plot_bmi_trends, bg="#2196F3", fg="white", font=("Arial", 12))
plot_button.grid(row=4, columnspan=2, pady=10)

# Label to display the result
result_label = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 12))
result_label.grid(row=5, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()