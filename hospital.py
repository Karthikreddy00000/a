"""
HOSPITAL MANAGEMENT SYSTEM (MySQL Version)
----------------------------------------
Features:
- Add Patient
- View Patients
- Search Patient
- Delete Patient
- MySQL Database
- GUI using Tkinter

This is a beginner-friendly mini project suitable for students.
"""

import tkinter as tk
from tkinter import messagebox
import mysql.connector

# DATABASE CONNECTION 

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Karthik@1402",  
        database="hospital_db"
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            pid VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            disease VARCHAR(100)
        )
    """)
    conn.commit()
    conn.close()


#  DATABASE FUNCTIONS 

def add_patient_db(pid, name, age, disease):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO patients VALUES (%s, %s, %s, %s)",
                (pid, name, age, disease))
    conn.commit()
    conn.close()


def get_all_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()
    return data


def search_patient_db(pid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE pid=%s", (pid,))
    data = cur.fetchone()
    conn.close()
    return data


def delete_patient_db(pid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE pid=%s", (pid,))
    conn.commit()
    conn.close()


#  GUI FUNCTIONS 

def add_patient():
    pid = entry_pid.get()
    name = entry_name.get()
    age = entry_age.get()
    disease = entry_disease.get()

    if pid == "" or name == "" or age == "" or disease == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        add_patient_db(pid, name, age, disease)
        messagebox.showinfo("Success", "Patient Added Successfully")
        clear_fields()
    except:
        messagebox.showerror("Error", "Patient ID already exists")


def view_patients():
    text_area.delete(1.0, tk.END)
    patients = get_all_patients()

    if not patients:
        text_area.insert(tk.END, "No Records Found")
        return

    text_area.insert(tk.END, "PID\tName\tAge\tDisease\n")
    text_area.insert(tk.END, "-------------------------------------\n")

    for pid, name, age, disease in patients:
        text_area.insert(tk.END, f"{pid}\t{name}\t{age}\t{disease}\n")


def search_patient():
    pid = entry_pid.get()
    text_area.delete(1.0, tk.END)

    data = search_patient_db(pid)
    if data:
        pid, name, age, disease = data
        text_area.insert(tk.END, "Patient Found:\n\n")
        text_area.insert(tk.END, f"ID: {pid}\nName: {name}\nAge: {age}\nDisease: {disease}")
    else:
        messagebox.showinfo("Info", "Patient Not Found")


def delete_patient():
    pid = entry_pid.get()
    delete_patient_db(pid)
    messagebox.showinfo("Deleted", "Patient Record Deleted")
    clear_fields()


def clear_fields():
    entry_pid.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_disease.delete(0, tk.END)


#  GUI DESIGN 

root = tk.Tk()
root.title("Hospital Management System")
root.geometry("650x450")

# Labels & Entries

tk.Label(root, text="Patient ID").place(x=20, y=20)
entry_pid = tk.Entry(root)
entry_pid.place(x=120, y=20)

tk.Label(root, text="Name").place(x=20, y=60)
entry_name = tk.Entry(root)
entry_name.place(x=120, y=60)

tk.Label(root, text="Age").place(x=20, y=100)
entry_age = tk.Entry(root)
entry_age.place(x=120, y=100)

tk.Label(root, text="Disease").place(x=20, y=140)
entry_disease = tk.Entry(root)
entry_disease.place(x=120, y=140)

# Buttons

tk.Button(root, text="Add Patient", width=15, command=add_patient).place(x=20, y=190)
tk.Button(root, text="View Patients", width=15, command=view_patients).place(x=160, y=190)
tk.Button(root, text="Search Patient", width=15, command=search_patient).place(x=300, y=190)
tk.Button(root, text="Delete Patient", width=15, command=delete_patient).place(x=440, y=190)

# Text Area
text_area = tk.Text(root, width=75, height=12)
text_area.place(x=20, y=240)

init_db()
root.mainloop()