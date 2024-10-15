import tkinter as tk
from tkinter import messagebox, filedialog
from pymongo import MongoClient
import csv

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Change this to your MongoDB connection string if needed
db = client['book_library']
books_collection = db['books']

# Functions to handle the database operations

def add_book():
    title = title_entry.get()
    author = author_entry.get()
    genre = genre_entry.get()
    isbn = isbn_entry.get()

    if not (title and author and genre and isbn):
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    # Insert the book into the collection
    books_collection.insert_one({
        "title": title,
        "author": author,
        "genre": genre,
        "isbn": isbn,
        "loaned": False
    })

    messagebox.showinfo("Success", "Book added successfully!")
    clear_fields()


def search_book():
    isbn = isbn_entry.get()

    if not isbn:
        messagebox.showwarning("Input Error", "Please enter the ISBN to search.")
        return

    book = books_collection.find_one({"isbn": isbn})

    if book:
        display_book(book)
    else:
        messagebox.showinfo("Not Found", "No book found with the given ISBN")


def remove_book():
    isbn = isbn_entry.get()

    if not isbn:
        messagebox.showwarning("Input Error", "Please enter the ISBN to remove the book.")
        return

    result = books_collection.delete_one({"isbn": isbn})

    if result.deleted_count > 0:
        messagebox.showinfo("Success", "Book removed successfully!")
        clear_fields()
    else:
        messagebox.showinfo("Not Found", "No book found with the given ISBN")


def display_book(book):
    clear_fields()
    title_entry.insert(0, book["title"])
    author_entry.insert(0, book["author"])
    genre_entry.insert(0, book["genre"])
    isbn_entry.insert(0, book["isbn"])


def clear_fields():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)


def loan_book():
    isbn = isbn_entry.get()

    if not isbn:
        messagebox.showwarning("Input Error", "Please enter the ISBN to loan the book.")
        return

    result = books_collection.update_one({"isbn": isbn}, {"$set": {"loaned": True}})

    if result.modified_count > 0:
        messagebox.showinfo("Success", "Book loaned successfully!")
        clear_fields()
    else:
        messagebox.showinfo("Not Found", "No book found with the given ISBN")


def return_book():
    isbn = isbn_entry.get()

    if not isbn:
        messagebox.showwarning("Input Error", "Please enter the ISBN to return the book.")
        return

    result = books_collection.update_one({"isbn": isbn}, {"$set": {"loaned": False}})

    if result.modified_count > 0:
        messagebox.showinfo("Success", "Book returned successfully!")
        clear_fields()
    else:
        messagebox.showinfo("Not Found", "No book found with the given ISBN")


def export_to_csv():
    # Ask the user where to save the CSV file
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    if filepath:
        books = books_collection.find()
        # Write the data to the CSV file
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            # Writing header
            writer.writerow(["Title", "Author", "Genre", "ISBN", "Loaned"])
            # Writing data rows
            for book in books:
                writer.writerow([book["title"], book["author"], book["genre"], book["isbn"], book["loaned"]])

        messagebox.showinfo("Success", "Database exported successfully as CSV!")


def import_from_csv():
    # Ask the user to select the CSV file
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if filepath:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if the book already exists using ISBN as the unique identifier
                if not books_collection.find_one({"isbn": row['ISBN']}):
                    books_collection.insert_one({
                        "title": row['Title'],
                        "author": row['Author'],
                        "genre": row['Genre'],
                        "isbn": row['ISBN'],
                        "loaned": row['Loaned'].lower() == 'true'
                    })

        messagebox.showinfo("Success", "Books imported successfully from CSV!")


# Tkinter GUI setup

root = tk.Tk()
root.title("Book Library")

# Labels
tk.Label(root, text="Book Title").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Author").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Genre").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="ISBN").grid(row=3, column=0, padx=10, pady=5)

# Entry fields
title_entry = tk.Entry(root)
author_entry = tk.Entry(root)
genre_entry = tk.Entry(root)
isbn_entry = tk.Entry(root)

title_entry.grid(row=0, column=1, padx=10, pady=5)
author_entry.grid(row=1, column=1, padx=10, pady=5)
genre_entry.grid(row=2, column=1, padx=10, pady=5)
isbn_entry.grid(row=3, column=1, padx=10, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Book", command=add_book)
search_button = tk.Button(root, text="Search Book", command=search_book)
remove_button = tk.Button(root, text="Remove Book", command=remove_book)
loan_button = tk.Button(root, text="Loan Book", command=loan_book)
return_button = tk.Button(root, text="Return Book", command=return_book)
export_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
import_button = tk.Button(root, text="Import from CSV", command=import_from_csv)

add_button.grid(row=4, column=0, padx=10, pady=5)
search_button.grid(row=4, column=1, padx=10, pady=5)
remove_button.grid(row=5, column=0, padx=10, pady=5)
loan_button.grid(row=5, column=1, padx=10, pady=5)
return_button.grid(row=6, column=0, padx=10, pady=5)
export_button.grid(row=6, column=1, padx=10, pady=5)
import_button.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
