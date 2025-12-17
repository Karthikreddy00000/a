import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# DATABASE CONNECTION

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        
        password="Karthik@1402",    
        database="placement_db"
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            department VARCHAR(50),
            cgpa FLOAT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies(
            company_id INT AUTO_INCREMENT PRIMARY KEY,
            company_name VARCHAR(100),
            package FLOAT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS placements(
            placement_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            company_id INT,
            date DATE,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(company_id) REFERENCES companies(company_id)
        )
    """)

    conn.commit()
    conn.close()

init_db()

# MAIN WINDOW

root = Tk()
root.title("College Placement Management System")
root.geometry("1000x600")


# VARIABLES

student_name = StringVar()
student_dept = StringVar()
student_cgpa = StringVar()

company_name = StringVar()
company_package = StringVar()

selected_student = StringVar()
selected_company = StringVar()

# FUNCTIONS

def add_student():
    if student_name.get() == "":
        messagebox.showerror("Error", "Enter student name")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students(name, department, cgpa) VALUES(%s,%s,%s)",
        (student_name.get(), student_dept.get(), student_cgpa.get())
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student Added")
    load_students()


def add_company():
    if company_name.get() == "":
        messagebox.showerror("Error", "Enter company name")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO companies(company_name, package) VALUES(%s,%s)",
        (company_name.get(), company_package.get())
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Company Added")
    load_companies()


def load_students():
    student_cb['values'] = []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT student_id, name FROM students")
    data = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
    student_cb['values'] = data
    conn.close()


def load_companies():
    company_cb['values'] = []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT company_id, company_name FROM companies")
    data = [f"{r[0]} - {r[1]}" for r in cur.fetchall()]
    company_cb['values'] = data
    conn.close()


def record_placement():
    if selected_student.get() == "" or selected_company.get() == "":
        messagebox.showerror("Error", "Select student and company")
        return

    sid = selected_student.get().split("-")[0].strip()
    cid = selected_company.get().split("-")[0].strip()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO placements(student_id, company_id, date) VALUES(%s,%s,%s)",
        (sid, cid, datetime.now().date())
    )
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Placement Recorded")
    load_placements()


def load_placements():
    for row in placement_table.get_children():
        placement_table.delete(row)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.name, s.department, c.company_name, c.package, p.date
        FROM placements p
        JOIN students s ON p.student_id=s.student_id
        JOIN companies c ON p.company_id=c.company_id
    """)

    for row in cur.fetchall():
        placement_table.insert("", END, values=row)
    conn.close()


# GUI LAYOUT

# Student Frame
stu_frame = LabelFrame(root, text="Add Student", padx=10, pady=10)
stu_frame.place(x=20, y=20, width=300, height=200)

Label(stu_frame, text="Name").grid(row=0, column=0)
Entry(stu_frame, textvariable=student_name).grid(row=0, column=1)

Label(stu_frame, text="Department").grid(row=1, column=0)
Entry(stu_frame, textvariable=student_dept).grid(row=1, column=1)

Label(stu_frame, text="CGPA").grid(row=2, column=0)
Entry(stu_frame, textvariable=student_cgpa).grid(row=2, column=1)

Button(stu_frame, text="Add Student", command=add_student).grid(row=3, column=0, columnspan=2, pady=10)

# Company Frame
comp_frame = LabelFrame(root, text="Add Company", padx=10, pady=10)
comp_frame.place(x=350, y=20, width=300, height=200)

Label(comp_frame, text="Company Name").grid(row=0, column=0)
Entry(comp_frame, textvariable=company_name).grid(row=0, column=1)

Label(comp_frame, text="Package (LPA)").grid(row=1, column=0)
Entry(comp_frame, textvariable=company_package).grid(row=1, column=1)

Button(comp_frame, text="Add Company", command=add_company).grid(row=2, column=0, columnspan=2, pady=10)

# Placement Frame
place_frame = LabelFrame(root, text="Record Placement", padx=10, pady=10)
place_frame.place(x=680, y=20, width=300, height=200)

Label(place_frame, text="Select Student").grid(row=0, column=0)
student_cb = ttk.Combobox(place_frame, textvariable=selected_student, state="readonly")
student_cb.grid(row=0, column=1)

Label(place_frame, text="Select Company").grid(row=1, column=0)
company_cb = ttk.Combobox(place_frame, textvariable=selected_company, state="readonly")
company_cb.grid(row=1, column=1)

Button(place_frame, text="Record Placement", command=record_placement).grid(row=2, column=0, columnspan=2, pady=10)

# Placement Table
place_table_frame = Frame(root, bd=3, relief=RIDGE)
place_table_frame.place(x=20, y=260, width=960, height=300)

placement_table = ttk.Treeview(place_table_frame,
                               columns=("name", "dept", "company", "package", "date"),
                               show="headings")

for col in ("name", "dept", "company", "package", "date"):
    placement_table.heading(col, text=col.title())

placement_table.pack(fill=BOTH, expand=1)

load_students()
load_companies()
load_placements()

root.mainloop()