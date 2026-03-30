import json
import tkinter as tk
from tkinter import messagebox

FILE = "projects.json"
selected_index = None

# =========================
# DATA HANDLER
# =========================
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

# =========================
# UI LOGIC
# =========================
def refresh_list():
    listbox.delete(0, tk.END)
    for p in load_data():
        listbox.insert(tk.END, p["name"])

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_source.delete(0, tk.END)
    entry_preview.delete(0, tk.END)

def fill_fields(event):
    global selected_index
    selected = listbox.curselection()
    if not selected:
        return

    selected_index = selected[0]
    data = load_data()[selected_index]

    clear_fields()
    entry_name.insert(0, data["name"])
    entry_desc.insert(0, data.get("description", ""))
    entry_source.insert(0, data["source"])
    entry_preview.insert(0, data.get("preview", ""))

# =========================
# CRUD
# =========================
def add_project():
    name = entry_name.get()
    desc = entry_desc.get()
    source = entry_source.get()
    preview = entry_preview.get()

    if not name or not source:
        messagebox.showwarning("Error", "Nama & Source wajib!")
        return

    data = load_data()
    data.append({
        "name": name,
        "description": desc,
        "source": source,
        "preview": preview
    })

    save_data(data)
    refresh_list()
    clear_fields()

def update_project():
    global selected_index
    if selected_index is None:
        messagebox.showwarning("Error", "Pilih project dulu!")
        return

    data = load_data()

    data[selected_index] = {
        "name": entry_name.get(),
        "description": entry_desc.get(),
        "source": entry_source.get(),
        "preview": entry_preview.get()
    }

    save_data(data)
    refresh_list()
    clear_fields()

def delete_project():
    global selected_index
    if selected_index is None:
        return

    if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus proyek ini?"):
        return

    data = load_data()
    data.pop(selected_index)

    save_data(data)
    refresh_list()
    clear_fields()

# =========================
# UI
# =========================
root = tk.Tk()
root.title("Ihsan Blog Monitor PRO - Editor Mode")
root.geometry("500x650")

# Menggunakan font yang lebih bersih untuk GUI
default_font = ("Arial", 10)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill="both", expand=True)

# Input fields
tk.Label(frame, text="Nama Project", font=("Arial", 10, "bold")).pack(anchor="w")
entry_name = tk.Entry(frame, font=default_font)
entry_name.pack(pady=(5, 15), fill="x")

tk.Label(frame, text="Deskripsi", font=("Arial", 10, "bold")).pack(anchor="w")
entry_desc = tk.Entry(frame, font=default_font)
entry_desc.pack(pady=(5, 15), fill="x")

tk.Label(frame, text="Source Code (GitHub URL)", font=("Arial", 10, "bold")).pack(anchor="w")
entry_source = tk.Entry(frame, font=default_font)
entry_source.pack(pady=(5, 15), fill="x")

tk.Label(frame, text="Preview Link (Live URL)", font=("Arial", 10, "bold")).pack(anchor="w")
entry_preview = tk.Entry(frame, font=default_font)
entry_preview.pack(pady=(5, 15), fill="x")

# BUTTON AREA
btn_frame = tk.Frame(frame)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Tambah", width=12, command=add_project, bg="#22c55e", fg="white", font=default_font).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", width=12, command=update_project, bg="#3b82f6", fg="white", font=default_font).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Hapus", width=12, command=delete_project, bg="#ef4444", fg="white", font=default_font).grid(row=0, column=2, padx=5)

# Separator
tk.Frame(frame, height=2, bd=1, relief="sunken").pack(fill="x", pady=20)

# LIST PROJECT
tk.Label(frame, text="Daftar Proyek:", font=("Arial", 10, "bold")).pack(anchor="w")
listbox = tk.Listbox(frame, font=default_font, height=12)
listbox.pack(fill="both", expand=True, pady=(5, 0))

# Scrollbar untuk listbox
scrollbar = tk.Scrollbar(listbox)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.bind("<<ListboxSelect>>", fill_fields)

refresh_list()

root.mainloop()