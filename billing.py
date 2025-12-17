import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


# MYSQL CONNECTION
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Karthik@1402",
        database="billing_db"
    )

# DATABASE INITIAL SETUP

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100),
            phone VARCHAR(15),
            items TEXT,
            total DECIMAL(10,2)
        )
    """)

    conn.commit()
    conn.close()

init_db()

# SAVE BILL TO DATABASE

def save_bill(name, phone, item_list, total):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO bills (customer_name, phone, items, total)
        VALUES (%s, %s, %s, %s)
    """, (name, phone, item_list, total))

    conn.commit()
    conn.close()

# MAIN APPLICATION (TKINTER)

root = Tk()
root.title("Billing System")
root.geometry("900x600")
root.config(bg="white")

# Variables

customer_name = StringVar()
customer_phone = StringVar()
item_name = StringVar()
item_price = StringVar()
item_qty = StringVar()

cart_items = []
grand_total = 0


# FUNCTIONS

def add_to_cart():
    global grand_total

    name = item_name.get()
    price = item_price.get()
    qty = item_qty.get()

    if name == "" or price == "" or qty == "":
        messagebox.showerror("Error", "Please fill all item details!")
        return

    try:
        price = float(price)
        qty = int(qty)
    except ValueError:
        messagebox.showerror("Error", "Invalid price or quantity")
        return

    total = price * qty

    cart_items.append({
        "name": name,
        "price": price,
        "qty": qty,
        "total": total
    })

    grand_total += total
    cart_table.insert("", END, values=(name, price, qty, total))
    update_total_label()

    item_name.set("")
    item_price.set("")
    item_qty.set("")

def update_total_label():
    total_label.config(text=f"Grand Total: ₹ {grand_total}")

def generate_bill():
    if not cart_items:
        messagebox.showerror("Error", "Cart is empty!")
        return

    name = customer_name.get()
    phone = customer_phone.get()

    if name == "" or phone == "":
        messagebox.showerror("Error", "Please enter customer details!")
        return

    bill_text.delete("1.0", END)
    bill_text.insert(END, "===== KRHS Billing System =====\n")
    bill_text.insert(END, f"Customer: {name}\n")
    bill_text.insert(END, f"Phone: {phone}\n")
    bill_text.insert(END, "--------------------------------\n")
    bill_text.insert(END, "Item\tQty\tPrice\tTotal\n")
    bill_text.insert(END, "--------------------------------\n")

    item_list_str = ""
    for item in cart_items:
        bill_text.insert(
            END,
            f"{item['name']}\t{item['qty']}\t{item['price']}\t{item['total']}\n"
        )
        item_list_str += f"{item['name']}({item['qty']}), "

    bill_text.insert(END, "--------------------------------\n")
    bill_text.insert(END, f"Grand Total: ₹ {grand_total}\n")
    bill_text.insert(END, "================================\n")

    save_bill(name, phone, item_list_str, grand_total)
    messagebox.showinfo("Success", "Bill saved successfully!")

def clear_all():
    global cart_items, grand_total

    customer_name.set("")
    customer_phone.set("")
    item_name.set("")
    item_price.set("")
    item_qty.set("")
    cart_items = []
    grand_total = 0

    for row in cart_table.get_children():
        cart_table.delete(row)

    update_total_label()
    bill_text.delete("1.0", END)


# GUI LAYOUT

customer_frame = Frame(root, bd=3, relief=RIDGE, padx=10, pady=10)
customer_frame.place(x=20, y=20, width=400, height=150)

Label(customer_frame, text="Customer Name").grid(row=0, column=0)
Entry(customer_frame, textvariable=customer_name).grid(row=0, column=1)

Label(customer_frame, text="Phone Number").grid(row=1, column=0)
Entry(customer_frame, textvariable=customer_phone).grid(row=1, column=1)

item_frame = Frame(root, bd=3, relief=RIDGE, padx=10, pady=10)
item_frame.place(x=20, y=200, width=400, height=200)

Label(item_frame, text="Item Name").grid(row=0, column=0)
Entry(item_frame, textvariable=item_name).grid(row=0, column=1)

Label(item_frame, text="Item Price").grid(row=1, column=0)
Entry(item_frame, textvariable=item_price).grid(row=1, column=1)

Label(item_frame, text="Quantity").grid(row=2, column=0)
Entry(item_frame, textvariable=item_qty).grid(row=2, column=1)

Button(item_frame, text="Add to Cart", bg="green", fg="white", command=add_to_cart)\
    .grid(row=3, column=0, columnspan=2, pady=10)

cart_frame = Frame(root, bd=3, relief=RIDGE)
cart_frame.place(x=450, y=20, width=430, height=300)

scroll_y = Scrollbar(cart_frame, orient=VERTICAL)
cart_table = ttk.Treeview(
    cart_frame,
    columns=("name", "price", "qty", "total"),
    show="headings",
    yscrollcommand=scroll_y.set
)
scroll_y.pack(side=RIGHT, fill=Y)

for col in ("name", "price", "qty", "total"):
    cart_table.heading(col, text=col.capitalize())

cart_table.pack(fill=BOTH, expand=1)

total_label = Label(root, text="Grand Total: ₹ 0", font=("Arial", 16), bg="white")
total_label.place(x=450, y=330)

bill_frame = Frame(root, bd=3, relief=RIDGE)
bill_frame.place(x=20, y=420, width=860, height=160)

bill_text = Text(bill_frame, font=("Courier", 10))
bill_text.pack(fill=BOTH, expand=1)

Button(root, text="Generate Bill", bg="blue", fg="white", command=generate_bill)\
    .place(x=450, y=370)
Button(root, text="Clear All", bg="red", fg="white", command=clear_all)\
    .place(x=580, y=370)

root.mainloop()
