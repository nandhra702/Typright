import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import triemodule  # Pybind11 extension
import sys
import os

import tempfile


# Write to the system's temp directory
debug_path = os.path.join(tempfile.gettempdir(), "debug_argv.txt")
with open(debug_path, "w") as f:
    f.write(str(sys.argv))

# Initialize Trie
my_trie = triemodule.Trie()
with open("D:\\Codes\\C++\\PROJECTS\\Typright\\wordlist.txt", "r") as f:
    for line in f:
        word = line.strip().lower()
        if word:
            my_trie.insert(word)

# ================== Functions ===================

def process_arguments():
         if len(sys.argv) > 1:
             argument_value = sys.argv[1]  # Get the first argument after the script name
             print("Received argument:", argument_value)
             open_file_arg(argument_value)
#             # You can then use this argument to modify your Tkinter application
#             # For example, update a label or configure a widget
#             label.config(text=f"Argument received: {argument_value}")
         else:
             print("No command-line arguments provided.")
             new_file()
#             label.config(text="No argument provided.")




# Handle PyInstaller path
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_suggestions(mode, word):
    if mode == "autocomplete":
        return my_trie.getWordsWithPrefix(word)
    elif mode == "spellcheck":
        return my_trie.suggestClosestWords(word)
    return []

def get_current_word():
    pos = textbox.index("insert")
    line_start = f"{pos.split('.')[0]}.0"
    line_text = textbox.get(line_start, pos)
    match = re.search(r"([\w']+)$", line_text)
    if match:
        word = match.group(1).lower().strip(".,!?;:\"()[]{}<>")
        return word
    return ""

def insert_selected_word():
    selection = listbox.curselection()
    if selection:
        selected = listbox.get(selection[0])
        word = get_current_word()
        if word:
            pos = textbox.index("insert")
            start = f"{pos.split('.')[0]}.{int(pos.split('.')[1]) - len(word)}"
            textbox.delete(start, pos)
            textbox.insert(start, selected)
        listbox.place_forget()
        textbox.focus_set()

def get_current_word_shorter():
    start_index = "end-31c"
    end_index = "end-1c"
    text = textbox.get(start_index, end_index)
    words = text.strip().split()
    return words[-1] if words else ""

def update_autocomplete_suggestions(word):
    if not word:
        listbox.place_forget()
        return

    suggestions = get_suggestions("autocomplete", word)
    if not suggestions:
        listbox.place_forget()
        return

    listbox.delete(0, tk.END)
    for suggestion in suggestions:
        listbox.insert(tk.END, suggestion)

    try:
        bbox = textbox.bbox("insert")
        if bbox:
            x, y, width, height = bbox
            listbox.place(x=x + 10, y=y + height + 5)
    except Exception:
        listbox.place_forget()

def on_key_release(event):
    char_count = len(textbox.get("1.0", "end-1c"))
    word = get_current_word() if char_count < 30 else get_current_word_shorter()
    update_autocomplete_suggestions(word)

def on_space(event):
    word = get_current_word()
    if word and not my_trie.search(word):
        underline_last_word(word)
    else:
        remove_underline_from_word(word)

def underline_last_word(word):
    text = textbox.get("1.0", tk.END)
    index = text.rfind(word)
    if index == -1:
        return

    before = text[:index]
    line = before.count("\n") + 1
    col = len(before.split("\n")[-1]) if "\n" in before else len(before)

    start = f"{line}.{col}"
    end = f"{line}.{col + len(word)}"

    textbox.tag_add("misspelled", start, end)
    textbox.tag_config("misspelled", underline=True, foreground="red")

def remove_underline_from_word(word):
    text = textbox.get("1.0", tk.END)
    index = text.rfind(word)
    if index == -1:
        return

    before = text[:index]
    line = before.count("\n") + 1
    col = len(before.split("\n")[-1]) if "\n" in before else len(before)

    start = f"{line}.{col}"
    end = f"{line}.{col + len(word)}"
    textbox.tag_remove("misspelled", start, end)

# ================== File Handling ===================

current_file_path = None

def new_file():
    global current_file_path
    textbox.delete(1.0, "end")
    current_file_path = None
    root.title("Typright - Untitled")

def open_file_arg(filename):
    global current_file_path
    filename = os.path.abspath(filename)
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return
    with open(filename, "r") as file:
        content = file.read()
        textbox.delete(1.0, "end")
        textbox.insert(1.0, content)
        current_file_path = filename
        root.title(f"Typright - {filename}")


def open_file():
    global current_file_path
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"),("Typright Files","*.type"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, "r") as file:
        content = file.read()
        textbox.delete(1.0, "end")
        textbox.insert(1.0, content)
        current_file_path = filepath
        root.title(f"Typright - {filepath}")

def save_file():
    if current_file_path is None:
        save_as_file()
    else:
        with open(current_file_path, "w") as file:
            file.write(textbox.get(1.0, "end-1c"))

def save_as_file():
    global current_file_path
    filepath = filedialog.asksaveasfilename(defaultextension=".type", filetypes=[("Text Files", "*.txt"),("Typright Files","*.type"), ("All Files", "*.*")])
    if not filepath:
        return
    with open(filepath, "w") as file:
        file.write(textbox.get(1.0, "end-1c"))
    current_file_path = filepath
    root.title(f"Typright - {filepath}")

def exit_editor():
    root.quit()

# ================== Night Mode ===================

dark_mode = False

def toggle_night_mode():
    global dark_mode
    dark_mode = not dark_mode

    bg = "#1e1e1e" if dark_mode else "white"
    fg = "#dcdcdc" if dark_mode else "black"
    textbox.config(bg=bg, fg=fg, insertbackground=fg)
    listbox.config(bg=bg, fg=fg)
    root.config(bg=bg)
    heading.config(bg=bg, fg=fg)

# ================== UI Setup ===================

root = tk.Tk()
root.title("Typright Notepad")
root.geometry("800x500")
root.minsize(600, 400)

style = ttk.Style()
style.theme_use("clam")

# Heading
heading = tk.Label(root, text="⚡🛠️ TYPRIGHT 🛠️⚡", font=("Helvetica", 20, "bold"), bg="#B3C6EA", fg="black")
heading.pack(pady=10)

# Text editor
textbox = tk.Text(root, wrap="word", undo=True, font=("Consolas", 12), bg="#B3C6EA", fg="black")
textbox.pack(expand=True, fill="both", padx=10, pady=5)
textbox.bind("<KeyRelease>", on_key_release)
textbox.bind("<space>", on_space)

# Suggestion box
listbox = tk.Listbox(root, height=5, font=("Consolas", 10), bg="white", fg="black")
listbox.place_forget()
textbox.bind("<Down>", lambda e: listbox.focus_set() or listbox.selection_set(0))
listbox.bind("<Return>", lambda e: insert_selected_word())
listbox.bind("<Double-Button-1>", lambda e: insert_selected_word())
listbox.bind("<Escape>", lambda e: listbox.place_forget())

# Menu
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)
menubar.add_cascade(label="File", menu=file_menu)

view_menu = tk.Menu(menubar, tearoff=0)
view_menu.add_command(label="Toggle Night Mode", command=toggle_night_mode)
menubar.add_cascade(label="View", menu=view_menu)
root.config(menu=menubar)


if __name__ == "__main__":
    process_arguments()  # ← this runs first
    root.mainloop()      # then the GUI loop starts
    

