import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# DATABASE CLASS (Encapsulation)
class BankDB:
    def __init__(self):
        self.__conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karthik@1402",
            database="bank_db"
        )
        self.__cursor = self.__conn.cursor()
        self.__create_table()

    def __create_table(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts(
                acc_no INT PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(15),
                balance DECIMAL(10,2)
            )
        """)
        self.__conn.commit()

    def insert_account(self, acc, name, phone, balance):
        self.__cursor.execute(
            "INSERT INTO accounts VALUES (%s,%s,%s,%s)",
            (acc, name, phone, balance)
        )
        self.__conn.commit()

    def update_balance(self, acc, amount):
        self.__cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE acc_no=%s",
            (amount, acc)
        )
        self.__conn.commit()

    def get_balance(self, acc):
        self.__cursor.execute(
            "SELECT balance FROM accounts WHERE acc_no=%s",
            (acc,)
        )
        return self.__cursor.fetchone()

    def get_all_accounts(self):
        self.__cursor.execute("SELECT * FROM accounts")
        return self.__cursor.fetchall()

    def close(self):
        self.__conn.close()

# ACCOUNT CLASS (Encapsulation)

class BankAccount:
    def __init__(self, acc_no, name, phone, balance):
        self.acc_no = acc_no
        self.name = name
        self.phone = phone
        self.__balance = balance  # PRIVATE VARIABLE

    def deposit(self, amt):
        if amt > 0:
            self.__balance += amt

    def withdraw(self, amt):
        if amt <= self.__balance:
            self.__balance -= amt
            return True
        return False

    def get_balance(self):
        return self.__balance


# GUI APPLICATION CLASS

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Account Management System")
        self.root.geometry("900x550")

        self.db = BankDB()
        self.__variables()
        self.__layout()
        self.load_accounts()

    def __variables(self):
        self.acc_no = StringVar()
        self.name = StringVar()
        self.phone = StringVar()
        self.balance = StringVar()
        self.amount = StringVar()

    def __layout(self):
        frame = Frame(self.root, bd=3, relief=RIDGE, padx=10, pady=10)
        frame.place(x=20, y=20, width=400, height=300)

        Label(frame, text="Account No").grid(row=0, column=0)
        Entry(frame, textvariable=self.acc_no).grid(row=0, column=1)

        Label(frame, text="Name").grid(row=1, column=0)
        Entry(frame, textvariable=self.name).grid(row=1, column=1)

        Label(frame, text="Phone").grid(row=2, column=0)
        Entry(frame, textvariable=self.phone).grid(row=2, column=1)

        Label(frame, text="Opening Balance").grid(row=3, column=0)
        Entry(frame, textvariable=self.balance).grid(row=3, column=1)

        Label(frame, text="Amount").grid(row=4, column=0)
        Entry(frame, textvariable=self.amount).grid(row=4, column=1)

        Button(frame, text="Create Account", command=self.create_account, bg="green", fg="white").grid(row=5, columnspan=2, pady=5)
        Button(frame, text="Deposit", command=self.deposit, bg="blue", fg="white").grid(row=6, columnspan=2, pady=5)
        Button(frame, text="Withdraw", command=self.withdraw, bg="orange", fg="white").grid(row=7, columnspan=2, pady=5)
        Button(frame, text="Check Balance", command=self.check_balance, bg="purple", fg="white").grid(row=8, columnspan=2, pady=5)

        table_frame = Frame(self.root, bd=3, relief=RIDGE)
        table_frame.place(x=450, y=20, width=800, height=400)

        self.table = ttk.Treeview(
            table_frame,
            columns=("acc", "name", "phone", "balance"),
            show="headings"
        )

        for col in ("acc", "name", "phone", "balance"):
            self.table.heading(col, text=col.capitalize())

        self.table.pack(fill=BOTH, expand=1)

    def create_account(self):
        try:
            acc = int(self.acc_no.get())
            bal = float(self.balance.get())
            self.db.insert_account(acc, self.name.get(), self.phone.get(), bal)
            messagebox.showinfo("Success", "Account created")
            self.load_accounts()
        except:
            messagebox.showerror("Error", "Account already exists or invalid input")

    def deposit(self):
        self.db.update_balance(self.acc_no.get(), float(self.amount.get()))
        messagebox.showinfo("Success", "Amount deposited")
        self.load_accounts()

    def withdraw(self):
        acc = self.acc_no.get()
        amt = float(self.amount.get())

        bal = self.db.get_balance(acc)
        if bal and bal[0] >= amt:
            self.db.update_balance(acc, -amt)
            messagebox.showinfo("Success", "Amount withdrawn")
            self.load_accounts()
        else:
            messagebox.showerror("Error", "Insufficient balance")

    def check_balance(self):
        bal = self.db.get_balance(self.acc_no.get())
        if bal:
            messagebox.showinfo("Balance", f"Current Balance: ₹ {bal[0]}")
        else:
            messagebox.showerror("Error", "Account not found")

    def load_accounts(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for acc in self.db.get_all_accounts():
            self.table.insert("", END, values=acc)


# RUN APPLICATION

root = Tk()
app = BankApp(root)
root.mainloop()
