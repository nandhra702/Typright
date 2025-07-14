import subprocess
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import filedialog
import os


import socket

def get_suggestions(mode, word):
    #here you are connecting to your cpp backend.
    s = socket.socket()
    s.connect(('localhost', 4000))
    s.sendall(f"{mode} {word}\n".encode())

    #you send the mode (autocomplete or spellchecker) and the word you want to check for
    data = b''
    while True:
        part = s.recv(1024)
        if not part:
            break
        data += part
    s.close()
    #now, s.recv(1024) tries to read up to 1024 bytes from the server.
    #If the server sends a response (e.g.,"mango\nmangrove\nmangoman\n"), they come in as raw bytes.
    return data.decode().splitlines()
  

def get_current_word(): #THIS HERE, READS THE TEXT BOX, STRIPS THE SPACES at begining and end, SPLITS THEM UP AND RETURNS THE LAST WORD
    text = textbox.get("1.0", END).strip()
    words = text.split()
    return words[-1] if words else ""


def get_current_word_shorter(): #function that simply starts to read from last 30 charcters
    #first, we need to get the size of words typed in the textbox.
    #if its smaller than a threshold, we use the original above function. If not, this function continues.
    start_index = "end-31c"  # 30 chars before the final character
    end_index = "end-1c"     # one character before the auto-added newline
    text= textbox.get(start_index, end_index)
    words = text.strip().split()
    return words[-1] if words else ""



def update_autocomplete_suggestions(word):
    if not word: #if its space or punctuation, it skips finding suggestions
        listbox.delete(0, END)
        return
    #else
    suggestions = get_suggestions("autocomplete", word)
    listbox.delete(0, END) #empties out the suggestion textbox and one by one, fills in the suggested words returned, prints them out.
    for suggestion in suggestions:
        listbox.insert(END, suggestion)


def on_key_release(event):
    #decides which function to utilize based on size of words in text box
    char_count = len(textbox.get("1.0", "end-1c")) 
    if char_count<30:
        word = get_current_word()
    else:
        word = get_current_word_shorter()

    update_autocomplete_suggestions(word)

def on_space(event):
    # Check the last word
    word = get_current_word()
    if not word:
        return
    suggestions = get_suggestions("spellcheck", word)
    if word not in suggestions:
        underline_last_word(word)

def underline_last_word(word):
    textbox.tag_remove("misspelled", "1.0", END)
    text = textbox.get("1.0", END).strip()
    index = text.rfind(word)
    if index != -1:
        start = f"1.{index}"
        end = f"1.{index + len(word)}"
        textbox.tag_add("misspelled", start, end)
        textbox.tag_config("misspelled", underline=True, foreground="red")

# UI setup
root = Tk()
root.title("Typright - Notepad")
root.geometry("700x500")
root.configure(bg="#f8f8f8")  # Soft background

# Load custom Bladerunner font from TTF file
font_path = os.path.join(os.path.dirname(__file__), "BLADRMF_.TTF")

try:
    bladerunner_font = tkFont.Font(file=font_path, size=14)
except Exception as e:
    print(f"[!] Failed to load Bladerunner font: {e}")
    bladerunner_font = ("Helvetica", 14)



# Heading
heading = Label(
    root,
    text="Typright",
    font=(bladerunner_font, 26, "bold"),
    fg="#333333",  # Soft black
    bg="#f8f8f8"
)
heading.pack(padx=20, pady=(30, 10))

#Top Menu
my_menu = Menu(root)
root.config(menu = my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label="New")
file_menu.add_separator()
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit")

# Fancy Textbox
textbox = Text(
    root,
    width=70,
    height=15,
    font=(bladerunner_font, 14),
    fg="#202020",
    bg="#ffffff",
    insertbackground="#2f8fff",  # Soft blue cursor
    relief=FLAT,
    undo = True,
    bd=2,
    highlightthickness=2,
    highlightbackground="#e0e0e0",
    highlightcolor="#2f8fff"
)
textbox.pack(padx=30, pady=(10, 10))


# Autocomplete Listbox
listbox = Listbox(
    root,
    height=4,
    bg="#fafafa",
    fg="#2f8fff",
    font=(bladerunner_font, 12),
    highlightthickness=1,
    selectbackground="#3997e3",
    selectforeground="#000000",
    borderwidth=0
)
listbox.pack(padx=30, pady=(0, 10))



textbox.bind("<KeyRelease>", on_key_release)
textbox.bind("<space>", on_space)



root.mainloop()
