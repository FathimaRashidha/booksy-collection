import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os

# ---------------- CONFIG ----------------
DATA_FILE = "data.json"
BG_IMAGE_PATH = "images/bg.jpg"

BOOK_CATEGORIES = {
    "Fiction": ["Fantasy","Science Fiction","Mystery/Thriller","Romance","Historical Fiction","Horror","Literary Fiction"],
    "Non-Fiction": ["Biography/Autobiography","Memoir","Self-Help","History","Science/Technology","Travel","Philosophy"],
    "Hybrid & Other": ["Poetry","Drama/Play","Children’s Books","Young Adult","Graphic Novels/Comics","Anthologies"]
}
LANGUAGES = ["English", "Tamil", "Sinhala"]

# ---------------- STORAGE ----------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE,"w") as f:
        json.dump(data, f, indent=4)

data = load_data()
for main in BOOK_CATEGORIES:
    if main not in data:
        data[main] = {}
    for sub in BOOK_CATEGORIES[main]:
        if sub not in data[main]:
            data[main][sub] = []

# ---------------- APP ----------------
root = tk.Tk()
root.title("📚 Booksy Collection")
root.geometry("700x600")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial",11), padding=6)
style.configure("TLabel", font=("Arial",11), background="#1e1e2f", foreground="white")

current_language = LANGUAGES[0]  # default

# ---------------- UTILS ----------------
def clear():
    for widget in root.winfo_children():
        widget.destroy()

def scroll_frame():
    container = tk.Frame(root, bg="#1e1e2f")
    canvas = tk.Canvas(container, bg="#1e1e2f", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    frame = tk.Frame(canvas, bg="#1e1e2f")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return frame

# ---------------- COVER PAGE ----------------
def cover_page():
    clear()
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    if os.path.exists(BG_IMAGE_PATH):
        img = Image.open(BG_IMAGE_PATH)

        def resize_bg(event):
            w, h = event.width, event.height
            resized = img.resize((w, h)).convert("RGBA")

            # Dim the image with a semi-transparent black overlay
            overlay = Image.new("RGBA", resized.size, (0, 0, 0, 120))
            blended = Image.alpha_composite(resized, overlay)

            canvas.bg_img = ImageTk.PhotoImage(blended)  # keep reference
            canvas.delete("all")
            canvas.create_image(0, 0, anchor="nw", image=canvas.bg_img)

            # Shadow text for clarity
            canvas.create_rectangle(w//2-250, h//2-40, w//2+250, h//2+40,
                        fill="black", stipple="gray50", outline="")
            canvas.create_text(w//2, h//2,
                   text="📚 Welcome to Booksy Collection",
                   font=("Arial", 28, "bold"),
                   fill="white",
                   anchor="center")


        canvas.bind("<Configure>", resize_bg)
    else:
        canvas.configure(bg="#cccccc")
        canvas.create_text(350, 300,
                           text="📚 Welcome to Booksy Collection",
                           font=("Arial", 28, "bold"),
                           fill="black",
                           anchor="center")

    root.after(5000, language_select)

# ---------------- LANGUAGE SELECTION ----------------
def language_select():
    global current_language
    clear()
    root.configure(bg="#1e1e2f")  # solid background
    ttk.Label(root, text="Select Language", font=("Arial",18), foreground="white", background="#1e1e2f").pack(pady=50)
    for lang in LANGUAGES:
        ttk.Button(root, text=lang, width=20, command=lambda l=lang: set_language(l)).pack(pady=10)
    ttk.Button(root, text="⬅ Back", command=cover_page).pack(pady=20)

def set_language(lang):
    global current_language
    current_language = lang
    dashboard()

# ---------------- DASHBOARD ----------------
def dashboard():
    clear()
    root.configure(bg="#1e1e2f")
    ttk.Label(root, text=f"📚 Booksy Collection - {current_language}", font=("Arial",18), foreground="white", background="#1e1e2f").pack(pady=20)
    for main in BOOK_CATEGORIES:
        ttk.Button(root, text=main, width=30, command=lambda m=main: show_subcategories(m)).pack(pady=6)
    ttk.Button(root, text="⬅ Back", command=language_select).pack(pady=10)

# ---------------- SUBCATEGORY VIEW ----------------
def show_subcategories(main):
    clear()
    root.configure(bg="#1e1e2f")
    ttk.Label(root, text=main, font=("Arial",16), foreground="white", background="#1e1e2f").pack(pady=10)
    for sub in BOOK_CATEGORIES[main]:
        ttk.Button(root, text=sub, width=30, command=lambda s=sub: open_category(main, s)).pack(pady=4)
    ttk.Button(root, text="⬅ Back", command=dashboard).pack(pady=10)

# ---------------- CATEGORY VIEW ----------------
def open_category(main, sub):
    clear()
    root.configure(bg="#1e1e2f")
    ttk.Label(root, text=f"{main} → {sub}", font=("Arial",14), foreground="white", background="#1e1e2f").pack(pady=10)
    frame = scroll_frame()
    books = data[main][sub]
    if not books:
        ttk.Label(frame, text="No books yet", foreground="white", background="#1e1e2f").pack()
    for book in books:
        text = (
            f"Title: {book['title']}\n"
            f"Author: {book['author']}\n"
            f"Inspiration: {book['inspire']}\n"
            f"Gain: {book['gain']}\n"
            f"Link: {book['link']}\n"
            "-----------------------------"
        )
        ttk.Label(frame, text=text, wraplength=650, justify="left", foreground="white", background="#1e1e2f").pack(anchor="w", pady=5)

    ttk.Button(root, text="➕ Suggest Book", command=lambda: upload_screen(main, sub)).pack(pady=5)
    ttk.Button(root, text="⬅ Back", command=lambda: show_subcategories(main)).pack()

# ---------------- UPLOAD SCREEN ----------------
def upload_screen(main, sub):
    clear()
    root.configure(bg="#1e1e2f")
    ttk.Label(root, text=f"Upload Book → {sub}", font=("Arial",16), foreground="white", background="#1e1e2f").pack(pady=10)
    entries = {}
    fields = ["Title","Author","Why inspiring","What you gained","Link/PDF"]
    for field in fields:
        ttk.Label(root, text=field, foreground="white", background="#1e1e2f").pack()
        e = ttk.Entry(root, width=60)
        e.pack(pady=3)
        entries[field] = e

    def save():
        title = entries["Title"].get().strip()
        if not title:
            messagebox.showerror("Error","Title is required")
            return
        book = {
            "title": title,
            "author": entries["Author"].get(),
            "inspire": entries["Why inspiring"].get(),
            "gain": entries["What you gained"].get(),
            "link": entries["Link/PDF"].get()
        }
        data[main][sub].append(book)
        save_data(data)
        messagebox.showinfo("Saved","Book added successfully!")
        open_category(main, sub)

    ttk.Button(root, text="Save Book", command=save).pack(pady=10)
    ttk.Button(root, text="⬅ Back", command=lambda: open_category(main, sub)).pack()

# ---------------- START ----------------
cover_page()
root.mainloop()
