import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_duplicate_files(directory):
    file_hashes = {}
    duplicate_files = []
    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = get_file_hash(file_path)
            if file_hash in file_hashes:
                duplicate_files.append((file_hashes[file_hash], file_path))
            else:
                file_hashes[file_hash] = file_path

                progress = len(file_hashes) / total_files * 100
            progress_var.set(progress)
            window.update_idletasks()
    return duplicate_files

def delete_file(file_path):
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False

def delete_selected_file():
    selected_item = file_listbox.curselection()
    if selected_item:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this file?")
        if confirmation:
            file_path = file_listbox.get(selected_item)
            if delete_file(file_path):
                file_listbox.delete(selected_item)
                messagebox.showinfo("Success", "The file has been successfully deleted.")
            else:
                messagebox.showerror("Error", "Impossible to delete the file.")
    else:
        messagebox.showwarning("Warning", "No file selected.")

def open_directory():
    directory = filedialog.askdirectory()
    if directory:
        file_listbox.delete(0, tk.END)
        progress_var.set(0)
        duplicate_files = get_duplicate_files(directory)
        if duplicate_files:
            for file_pair in duplicate_files:
                file_listbox.insert(tk.END, file_pair[0])
                file_listbox.insert(tk.END, file_pair[1])
        else:
            messagebox.showinfo("Information", "No duplicate file was found here.")

def show_preview():
    selected_item = file_listbox.curselection()
    if selected_item:
        file_path = file_listbox.get(selected_item)
        if os.path.isfile(file_path):
            try:
                image = Image.open(file_path)
                image.show()
            except IOError:
                messagebox.showwarning("Warning", "Unable to open the file preview.")
        else:
            messagebox.showwarning("Warning", "The selected file is not valid.")
    else:
        messagebox.showwarning("Warning", "No file selected.")

window = tk.Tk()
window.title("Duplicate file manager")
window.geometry("600x400")
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox = tk.Listbox(window, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
file_listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=file_listbox.yview)
delete_button = tk.Button(window, text="Delete", command=delete_selected_file)
delete_button.pack(side=tk.BOTTOM)
preview_button = tk.Button(window, text="Preview", command=show_preview)
preview_button.pack(side=tk.BOTTOM)
open_button = tk.Button(window, text="Open directory", command=open_directory)
open_button.pack(side=tk.BOTTOM)
progress_var = tk.DoubleVar()
progress_bar = Progressbar(window, variable=progress_var, maximum=100)
progress_bar.pack(side=tk.BOTTOM, fill=tk.X)
window.mainloop()
