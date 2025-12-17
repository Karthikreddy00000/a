import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# DATABASE 

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="Karthik@1402",  
        database="attendance_db"
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Student table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            roll VARCHAR(50) UNIQUE NOT NULL
        )
    """)

    # Attendance table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            att_id INT AUTO_INCREMENT PRIMARY KEY,
            roll VARCHAR(50),
            name VARCHAR(100),
            status VARCHAR(20),
            date VARCHAR(20)
        )
    """)

    conn.commit()
    conn.close()

# Call DB init
init_db()

# MAIN WINDOW
root = Tk()
root.title("Attendance System (MySQL)")
root.geometry("900x600")
root.config(bg="white")

# VARIABLES

student_name = StringVar()
student_roll = StringVar()

attendance_roll = StringVar()
attendance_status = StringVar(value="Present")
attendance_date = StringVar()


# FUNCTIONS

def register_student():
    name = student_name.get()
    roll = student_roll.get()

    if name == "" or roll == "":
        messagebox.showerror("Error", "Please enter student's name and roll number!")
        return

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO students(name, roll) VALUES (%s, %s)",
            (name, roll)
        )
        conn.commit()
        messagebox.showinfo("Success", "Student registered successfully!")
        student_name.set("")
        student_roll.set("")
        load_students()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")
    finally:
        conn.close()


def load_students():
    for row in student_table.get_children():
        student_table.delete(row)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")

    for row in cur.fetchall():
        student_table.insert("", END, values=row)

    conn.close()


def mark_attendance():
    roll = attendance_roll.get()
    status = attendance_status.get()
    date = attendance_date.get()

    if roll == "" or date == "":
        messagebox.showerror("Error", "Please select roll number and enter date!")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM students WHERE roll=%s", (roll,))
    data = cur.fetchone()

    if data is None:
        messagebox.showerror("Error", "Roll number not found!")
        conn.close()
        return

    name = data[0]

    cur.execute(
        "INSERT INTO attendance(roll, name, status, date) VALUES (%s, %s, %s, %s)",
        (roll, name, status, date)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Attendance marked successfully!")
    attendance_roll.set("")
    attendance_date.set("")
    load_attendance()


def load_attendance():
    for row in attendance_table.get_children():
        attendance_table.delete(row)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM attendance")

    for row in cur.fetchall():
        attendance_table.insert("", END, values=row)

    conn.close()

# GUI LAYOUT

#  Register Student Frame 
reg_frame = Frame(root, bd=3, relief=RIDGE, padx=10, pady=10)
reg_frame.place(x=20, y=20, width=350, height=200)

Label(reg_frame, text="Student Name").grid(row=0, column=0)
Entry(reg_frame, textvariable=student_name).grid(row=0, column=1)

Label(reg_frame, text="Roll Number").grid(row=1, column=0)
Entry(reg_frame, textvariable=student_roll).grid(row=1, column=1)

Button(reg_frame, text="Register Student", bg="green", fg="white",
       command=register_student).grid(row=2, column=0, columnspan=2, pady=10)

#  Student List 
student_frame = Frame(root, bd=3, relief=RIDGE)
student_frame.place(x=20, y=240, width=350, height=320)

Label(student_frame, text="Registered Students").pack()

st_scroll = Scrollbar(student_frame, orient=VERTICAL)
student_table = ttk.Treeview(student_frame, columns=("id", "name", "roll"),
                             show="headings", yscrollcommand=st_scroll.set)
st_scroll.pack(side=RIGHT, fill=Y)

student_table.heading("id", text="ID")
student_table.heading("name", text="Name")
student_table.heading("roll", text="Roll No")

student_table.column("id", width=30)
student_table.column("name", width=150)
student_table.column("roll", width=100)

student_table.pack(fill=BOTH, expand=1)

load_students()

# Mark Attendance Frame 
att_frame = Frame(root, bd=3, relief=RIDGE, padx=10, pady=10)
att_frame.place(x=400, y=20, width=470, height=200)

Label(att_frame, text="Roll No").grid(row=0, column=0)
Entry(att_frame, textvariable=attendance_roll).grid(row=0, column=1)

Label(att_frame, text="Status").grid(row=1, column=0)
OptionMenu(att_frame, attendance_status, "Present", "Absent").grid(row=1, column=1)

Label(att_frame, text="Date (DD-MM-YYYY)").grid(row=2, column=0)
Entry(att_frame, textvariable=attendance_date).grid(row=2, column=1)

Button(att_frame, text="Mark Attendance", bg="blue", fg="white",
       command=mark_attendance).grid(row=3, column=0, columnspan=2, pady=10)

#  Attendance Table
att_table_frame = Frame(root, bd=3, relief=RIDGE)
att_table_frame.place(x=400, y=240, width=470, height=320)

Label(att_table_frame, text="Attendance Records").pack()

att_scroll = Scrollbar(att_table_frame, orient=VERTICAL)
attendance_table = ttk.Treeview(att_table_frame,
                                columns=("id", "roll", "name", "status", "date"),
                                show="headings", yscrollcommand=att_scroll.set)
att_scroll.pack(side=RIGHT, fill=Y)

attendance_table.heading("id", text="ID")
attendance_table.heading("roll", text="Roll")
attendance_table.heading("name", text="Name")
attendance_table.heading("status", text="Status")
attendance_table.heading("date", text="Date")

attendance_table.column("id", width=30)
attendance_table.column("roll", width=80)
attendance_table.column("name", width=140)
attendance_table.column("status", width=80)
attendance_table.column("date", width=100)

attendance_table.pack(fill=BOTH, expand=1)

load_attendance()

root.mainloop()