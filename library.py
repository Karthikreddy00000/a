import os
from tkinter import *
from tkinter import messagebox

FILE = "library.txt"


# File Handling

def load_books():
    books = []
    if not os.path.exists(FILE):
        return books

    with open(FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                book_id, title, author, status = line.split("|")
                books.append({
                    "id": book_id,
                    "title": title,
                    "author": author,
                    "status": status
                })
    return books


def save_books():
    with open(FILE, "w") as f:
        for b in books:
            f.write(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}\n")



# Functions
def add_book():
    bid = book_id.get().strip()
    title = book_title.get().strip()
    author = book_author.get().strip()

    if bid == "" or title == "" or author == "":
        messagebox.showerror("Error", "All fields required")
        return

    for b in books:
        if b["id"] == bid:
            messagebox.showerror("Error", "Book ID already exists")
            return

    books.append({
        "id": bid,
        "title": title,
        "author": author,
        "status": "available"
    })
    save_books()
    clear_entries()
    load_list()
    messagebox.showinfo("Success", "Book added successfully")


def load_list():
    listbox.delete(0, END)
    for b in books:
        listbox.insert(END, f"{b['id']} | {b['title']} | {b['author']} | {b['status']}")


def search_book():
    query = search_var.get().lower()
    listbox.delete(0, END)

    for b in books:
        if query in b["id"].lower() or query in b["title"].lower():
            listbox.insert(END, f"{b['id']} | {b['title']} | {b['author']} | {b['status']}")


def issue_book():
    bid = book_id.get().strip()
    for b in books:
        if b["id"] == bid:
            if b["status"] == "issued":
                messagebox.showwarning("Warning", "Book already issued")
            else:
                b["status"] = "issued"
                save_books()
                load_list()
                messagebox.showinfo("Success", "Book issued")
            return
    messagebox.showerror("Error", "Book not found")


def return_book():
    bid = book_id.get().strip()
    for b in books:
        if b["id"] == bid:
            if b["status"] == "available":
                messagebox.showwarning("Warning", "Book not issued")
            else:
                b["status"] = "available"
                save_books()
                load_list()
                messagebox.showinfo("Success", "Book returned")
            return
    messagebox.showerror("Error", "Book not found")


def delete_book():
    bid = book_id.get().strip()
    for i, b in enumerate(books):
        if b["id"] == bid:
            if messagebox.askyesno("Confirm", "Delete this book?"):
                books.pop(i)
                save_books()
                load_list()
                messagebox.showinfo("Deleted", "Book deleted")
            return
    messagebox.showerror("Error", "Book not found")


def clear_entries():
    book_id.set("")
    book_title.set("")
    book_author.set("")



# GUI

books = load_books()

root = Tk()
root.title("Library Management System")
root.geometry("800x500")
root.config(bg="white")

book_id = StringVar()
book_title = StringVar()
book_author = StringVar()
search_var = StringVar()

#  Form Frame 
frame = Frame(root, bd=3, relief=RIDGE, padx=10, pady=10)
frame.place(x=20, y=20, width=350, height=260)

Label(frame, text="Book ID").grid(row=0, column=0)
Entry(frame, textvariable=book_id).grid(row=0, column=1)

Label(frame, text="Title").grid(row=1, column=0)
Entry(frame, textvariable=book_title).grid(row=1, column=1)

Label(frame, text="Author").grid(row=2, column=0)
Entry(frame, textvariable=book_author).grid(row=2, column=1)

Button(frame, text="Add Book", width=15, bg="green", fg="white", command=add_book).grid(row=3, column=0, columnspan=2, pady=5)
Button(frame, text="Issue Book", width=15, bg="blue", fg="white", command=issue_book).grid(row=4, column=0, columnspan=2, pady=5)
Button(frame, text="Return Book", width=15, bg="orange", fg="white", command=return_book).grid(row=5, column=0, columnspan=2, pady=5)
Button(frame, text="Delete Book", width=15, bg="red", fg="white", command=delete_book).grid(row=6, column=0, columnspan=2, pady=5)

#  Search 
Label(root, text="Search").place(x=420, y=20)
Entry(root, textvariable=search_var).place(x=480, y=20)
Button(root, text="Search", command=search_book).place(x=650, y=18)
Button(root, text="View All", command=load_list).place(x=720, y=18)

#  Listbox 
listbox = Listbox(root, width=70, height=20)
listbox.place(x=400, y=60)

load_list()

root.mainloop()
