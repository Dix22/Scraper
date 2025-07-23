import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import pyperclip  # pip install pyperclip

def scrape():
    url = url_entry.get().strip()

    if not url.startswith("http"):
        update_status("⚠️ Please enter a valid URL starting with http or https.")
        return

    update_status("🔄 Processing...")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        update_status("❌ Failed to access the page.")
        messagebox.showerror("Error", f"Unable to access the page:\n{e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    texts = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
        text = tag.get_text(strip=True)
        if text:
            if tag.name.startswith("h"):
                texts.append(f"[{tag.name.upper()}] {text}\n")
            else:
                texts.append(text + "\n")

    domain = urlparse(url).netloc.replace("www.", "").replace(".", "_")
    filename = f"{domain}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for line in texts:
            f.write(line + "\n")

    update_status(f"✅ Saved as: {filename}")
    messagebox.showinfo("Success", f"Content saved to:\n{filename}")
    open_button.config(state="normal")
    copy_button.config(state="normal")
    current_file.set(filename)

def open_file():
    path = current_file.get()
    if os.path.exists(path):
        os.system(f'notepad "{path}"')

def copy_path():
    path = current_file.get()
    if path:
        pyperclip.copy(os.path.abspath(path))
        messagebox.showinfo("Copied", f"Path copied to clipboard:\n{path}")

def update_status(text):
    status_var.set(text)

# --- GUI SETUP ---
window = tk.Tk()
window.title("🕸️ Interactive Web Scraper")
window.geometry("530x300")
window.resizable(False, False)
window.configure(bg="#f4f4f4")

# URL Input
tk.Label(window, text="🔗 Enter the website URL:", bg="#f4f4f4", font=("Segoe UI", 11)).pack(pady=(15, 5))
url_entry = tk.Entry(window, width=60, font=("Segoe UI", 10))
url_entry.pack()

# Buttons
tk.Button(window, text="🌐 Scrape and Save", command=scrape, bg="#4CAF50", fg="white", width=20, font=("Segoe UI", 10)).pack(pady=15)

open_button = tk.Button(window, text="📂 Open .txt file", command=open_file, bg="#2196F3", fg="white", width=20, font=("Segoe UI", 10), state="disabled")
open_button.pack(pady=5)

copy_button = tk.Button(window, text="📋 Copy file path", command=copy_path, bg="#FF9800", fg="white", width=20, font=("Segoe UI", 10), state="disabled")
copy_button.pack(pady=5)

# Status
status_var = tk.StringVar()
status_var.set("Waiting for input...")
tk.Label(window, textvariable=status_var, bg="#f4f4f4", fg="gray", font=("Segoe UI", 10)).pack(pady=15)

# Store current file path
current_file = tk.StringVar()

window.mainloop()