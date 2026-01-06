import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

FILENAME = "students.json"

# ---------- Data Functions ----------
def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

def save_data(students):
    with open(FILENAME, "w") as file:
        json.dump(students, file, indent=4)

# ---------- Grade & CGPA Calculation ----------
def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"

def calculate_cgpa(percentage):
    return round(percentage / 10, 2)

# ---------- GUI Functions ----------
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    students = load_data()
    for student in students:
        total = sum(student["marks"])
        percentage = total / 5
        grade = calculate_grade(percentage)
        cgpa = calculate_cgpa(percentage)
        tree.insert("", "end", iid=student["roll"],
                    values=(student["roll"], student["name"], *student["marks"], total, f"{percentage:.2f}", grade, cgpa))

def add_student():
    name = entry_name.get().strip()
    roll = entry_roll.get().strip()
    if not name or not roll:
        messagebox.showerror("Error", "Name and Roll Number cannot be empty!")
        return
    try:
        marks_list = [float(entry_math.get()), float(entry_ds.get()), float(entry_dbms.get()),
                      float(entry_os.get()), float(entry_cn.get())]
    except:
        messagebox.showerror("Error", "Enter valid numeric marks for all subjects!")
        return
    # Marks validation
    for mark in marks_list:
        if mark < 0 or mark > 100:
            messagebox.showerror("Error", "Each mark must be between 0 and 100!")
            return

    students = load_data()
    if any(s['roll'] == roll for s in students):
        messagebox.showerror("Error", "Roll Number already exists!")
        return

    students.append({"name": name, "roll": roll, "marks": marks_list})
    save_data(students)
    messagebox.showinfo("Success", f"Student {name} added!")
    clear_entries()
    refresh_table()

def select_student(event):
    selected = tree.focus()
    if selected:
        student = tree.item(selected, "values")
        # Fill entries with selected student's data
        entry_roll.delete(0, tk.END)
        entry_roll.insert(0, student[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, student[1])
        entry_math.delete(0, tk.END)
        entry_math.insert(0, student[2])
        entry_ds.delete(0, tk.END)
        entry_ds.insert(0, student[3])
        entry_dbms.delete(0, tk.END)
        entry_dbms.insert(0, student[4])
        entry_os.delete(0, tk.END)
        entry_os.insert(0, student[5])
        entry_cn.delete(0, tk.END)
        entry_cn.insert(0, student[6])

def update_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student from the table to update!")
        return
    students = load_data()
    for student in students:
        if student["roll"] == selected:
            name = entry_name.get().strip()
            if name:
                student["name"] = name
            try:
                marks_list = [float(entry_math.get()), float(entry_ds.get()), float(entry_dbms.get()),
                              float(entry_os.get()), float(entry_cn.get())]
            except:
                messagebox.showerror("Error", "Invalid marks! Update failed.")
                return
            # Marks validation
            for mark in marks_list:
                if mark < 0 or mark > 100:
                    messagebox.showerror("Error", "Each mark must be between 0 and 100!")
                    return
            student["marks"] = marks_list
            save_data(students)
            messagebox.showinfo("Success", "Record updated!")
            clear_entries()
            refresh_table()
            return

def delete_student():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a student from the table to delete!")
        return
    students = load_data()
    new_students = [s for s in students if s["roll"] != selected]
    save_data(new_students)
    messagebox.showinfo("Success", "Record deleted!")
    clear_entries()
    refresh_table()

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_math.delete(0, tk.END)
    entry_ds.delete(0, tk.END)
    entry_dbms.delete(0, tk.END)
    entry_os.delete(0, tk.END)
    entry_cn.delete(0, tk.END)

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Mumbai University Style Result Management System")
root.geometry("1200x550")
root.configure(bg="#f0f8ff")

# Title
title = tk.Label(root, text="💻 Engineer Result Management System (MU Style) 💻",
                 font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#1e90ff")
title.pack(pady=10)

# Entry Frame
frame_entry = tk.Frame(root, bg="#e6f2ff", bd=2, relief=tk.RIDGE)
frame_entry.pack(padx=10, pady=10, fill=tk.X)

# Labels & Entries
tk.Label(frame_entry, text="Name", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_entry)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Roll No", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5)
entry_roll = tk.Entry(frame_entry)
entry_roll.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_entry, text="Mathematics", bg="#e6f2ff").grid(row=1, column=0, padx=5, pady=5)
entry_math = tk.Entry(frame_entry)
entry_math.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Data Structures", bg="#e6f2ff").grid(row=1, column=2, padx=5, pady=5)
entry_ds = tk.Entry(frame_entry)
entry_ds.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame_entry, text="DBMS", bg="#e6f2ff").grid(row=2, column=0, padx=5, pady=5)
entry_dbms = tk.Entry(frame_entry)
entry_dbms.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_entry, text="Operating Systems", bg="#e6f2ff").grid(row=2, column=2, padx=5, pady=5)
entry_os = tk.Entry(frame_entry)
entry_os.grid(row=2, column=3, padx=5, pady=5)

tk.Label(frame_entry, text="Computer Networks", bg="#e6f2ff").grid(row=3, column=0, padx=5, pady=5)
entry_cn = tk.Entry(frame_entry)
entry_cn.grid(row=3, column=1, padx=5, pady=5)

# Button Frame
frame_buttons = tk.Frame(root, bg="#f0f8ff")
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Add Student", bg="#1e90ff", fg="white", width=15, command=add_student).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update Student", bg="#ff8c00", fg="white", width=15, command=update_student).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete Student", bg="#ff4c4c", fg="white", width=15, command=delete_student).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear Fields", bg="#6a5acd", fg="white", width=15, command=clear_entries).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Refresh Table", bg="#32cd32", fg="white", width=15, command=refresh_table).grid(row=0, column=4, padx=5)

# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("Roll", "Name", "Mathematics", "DS", "DBMS", "OS", "CN", "Total", "Percentage", "Grade", "CGPA")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# Bind selection
tree.bind("<ButtonRelease-1>", select_student)

refresh_table()
root.mainloop()
