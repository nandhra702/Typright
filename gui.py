from tkinter import *
import tkinter as tk
import re
import triemodule  # this is the pybind11 C++ extension
from tkinter import filedialog, messagebox


# Create and initialize Trie instance
my_trie = triemodule.Trie()

# Load dictionary
with open("wordlist.txt", "r") as f:
    for line in f:
        word = line.strip().lower()
        if word:
            my_trie.insert(word)

# GUI logic
def get_suggestions(mode, word):
    if mode == "autocomplete":
        return my_trie.getWordsWithPrefix(word)
    elif mode == "spellcheck":
        return my_trie.suggestClosestWords(word)
    return []



def get_current_word():
    # Get cursor position and current line text
    pos = textbox.index("insert")
    line_start = f"{pos.split('.')[0]}.0"
    line_text = textbox.get(line_start, pos)

    # Extract the last word using regex (preserves contractions like don't)
    match = re.search(r"([\w']+)$", line_text)
    if match:
        word = match.group(1).lower()
        word = match.group(1).lower()
        # Optional: strip trailing punctuation if still present
        word = word.strip(".,!?;:\"()[]{}<>")
        return word
    return ""

def insert_selected_word():
    selection = listbox.curselection()
    if selection:
        selected = listbox.get(selection[0])
        word = get_current_word()
        if word:
            pos = textbox.index("insert")
            line_start = f"{pos.split('.')[0]}.0"
            line_text = textbox.get(line_start, pos)
            match = re.search(r"([\w']+)$", line_text)
            if match:
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
        listbox.delete(0, END)
        return
    suggestions = get_suggestions("autocomplete", word)
    listbox.delete(0, END)
    for suggestion in suggestions:
        listbox.insert(END, suggestion)

def on_key_release(event):
    char_count = len(textbox.get("1.0", "end-1c"))
    if char_count < 30:
        word = get_current_word()
    else:
        word = get_current_word_shorter()
    update_autocomplete_suggestions(word)

def on_space(event):
    word = get_current_word()
    if not word:
        return

    # Check using Trie
    if not my_trie.search(word):
        underline_last_word(word)
    else:
        remove_underline_from_word(word)


def underline_last_word(word):
    text = textbox.get("1.0", END)
    index = text.rfind(word)

    if index == -1:
        return

    # Find the line and column number for the word
    before_word = text[:index]
    line = before_word.count("\n") + 1
    if "\n" in before_word:
        col = len(before_word.split("\n")[-1])
    else:
        col = len(before_word)

    start = f"{line}.{col}"
    end = f"{line}.{col + len(word)}"

    textbox.tag_add("misspelled", start, end)
    textbox.tag_config("misspelled", underline=True, foreground="red")

def update_autocomplete_suggestions(word):
    if not word:
        listbox.place_forget()
        return

    suggestions = get_suggestions("autocomplete", word)
    if not suggestions:
        listbox.place_forget()
        return

    listbox.delete(0, END)
    for suggestion in suggestions:
        listbox.insert(END, suggestion)

    # Get screen position of the cursor
    try:
        bbox = textbox.bbox("insert")
        if bbox:
            x, y, width, height = bbox
            listbox.place(x=x, y=y + height + 5)
    except Exception:
        listbox.place_forget()



def remove_underline_from_word(word):
    text = textbox.get("1.0", END)
    index = text.rfind(word)

    if index == -1:
        return

    before_word = text[:index]
    line = before_word.count("\n") + 1
    if "\n" in before_word:
        col = len(before_word.split("\n")[-1])
    else:
        col = len(before_word)

    start = f"{line}.{col}"
    end = f"{line}.{col + len(word)}"
    textbox.tag_remove("misspelled", start, end)


# UI Setup
root = Tk()
root.title("Typright Notepad")
root.geometry("400x300")


heading = Label(
    root,
    text="TYPRIGHT",
    font=("Helvetica", 19),
    fg="black",
    bg="white"
)
heading.pack(padx=20, pady=(30, 10))

textbox = Text(
    root,
    width=80,
    height=10,
    fg="black",
    bg="lightblue"
)
textbox = tk.Text(root, wrap="word", undo=True)
textbox.pack(expand=True, fill="both")
textbox.bind("<KeyRelease>", on_key_release)
textbox.bind("<space>", on_space)

listbox = Listbox(root, height=4)
listbox.place_forget()  # Initially hidden

textbox.bind("<Down>", lambda e: listbox.focus_set() or listbox.selection_set(0))
listbox.bind("<Return>", lambda e: insert_selected_word())
listbox.bind("<Double-Button-1>", lambda e: insert_selected_word())
listbox.bind("<Escape>", lambda e: listbox.place_forget())



# //////////////////////////// functionality
current_file_path = None

def new_file():
    global current_file_path
    textbox.delete(1.0, "end")
    current_file_path = None
    root.title("Typright - Untitled")

def open_file():
    global current_file_path
    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "r") as input_file:
        content = input_file.read()
        textbox.delete(1.0, "end")
        textbox.insert(1.0, content)
        current_file_path = filepath
        root.title(f"Typright - {filepath}")

def save_file():
    global current_file_path
    if current_file_path is None:
        save_as_file()
    else:
        with open(current_file_path, "w") as output_file:
            output_file.write(textbox.get(1.0, "end-1c"))

def save_as_file():
    global current_file_path
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        output_file.write(textbox.get(1.0, "end-1c"))
    current_file_path = filepath
    root.title(f"Typright - {filepath}")

def exit_editor():
    root.quit()





menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)
menubar.add_cascade(label="File", menu=file_menu)

root.config(menu=menubar)

# ////////////////////////////// ADDING FILE FUNCTIONALITY

# Global variable to track the current open file



root.mainloop()

