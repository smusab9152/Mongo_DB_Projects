import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Change this to your MongoDB connection string if needed
db = client['todo_list']
tasks_collection = db['tasks']

# Functions to handle the database operations

def add_task():
    task = task_entry.get()
    due_date = due_date_entry.get()
    priority = priority_entry.get()

    if not (task and due_date and priority):
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    # Insert the task into the collection
    tasks_collection.insert_one({
        "task": task,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    })

    messagebox.showinfo("Success", "Task added successfully!")
    clear_fields()
    refresh_task_list()


def remove_task():
    task = task_entry.get()

    if not task:
        messagebox.showwarning("Input Error", "Please enter the task name to remove.")
        return

    result = tasks_collection.delete_one({"task": task})

    if result.deleted_count > 0:
        messagebox.showinfo("Success", "Task removed successfully!")
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showinfo("Not Found", "No task found with the given name")


def mark_complete():
    task = task_entry.get()

    if not task:
        messagebox.showwarning("Input Error", "Please enter the task name to mark as complete.")
        return

    result = tasks_collection.update_one({"task": task}, {"$set": {"completed": True}})

    if result.modified_count > 0:
        messagebox.showinfo("Success", "Task marked as complete!")
        clear_fields()
        refresh_task_list()
    else:
        messagebox.showinfo("Not Found", "No task found with the given name")


def clear_fields():
    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)


def refresh_task_list():
    tasks = tasks_collection.find()
    task_list.delete(0, tk.END)
    
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        task_list.insert(tk.END, f"{task['task']} | Due: {task['due_date']} | Priority: {task['priority']} | Completed: {status}")


# Tkinter GUI setup

root = tk.Tk()
root.title("To-Do List")

# Labels
tk.Label(root, text="Task").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Due Date").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Priority").grid(row=2, column=0, padx=10, pady=5)

# Entry fields
task_entry = tk.Entry(root)
due_date_entry = tk.Entry(root)
priority_entry = tk.Entry(root)

task_entry.grid(row=0, column=1, padx=10, pady=5)
due_date_entry.grid(row=1, column=1, padx=10, pady=5)
priority_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task)
remove_button = tk.Button(root, text="Remove Task", command=remove_task)
complete_button = tk.Button(root, text="Mark as Complete", command=mark_complete)

add_button.grid(row=3, column=0, padx=10, pady=5)
remove_button.grid(row=3, column=1, padx=10, pady=5)
complete_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Task list display
task_list = tk.Listbox(root, width=80, height=10)
task_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

refresh_task_list()

root.mainloop()
