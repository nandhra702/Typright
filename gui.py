import subprocess
from tkinter import *


import socket

def get_suggestions(mode, word):
    s = socket.socket()
    s.connect(('localhost', 4000))
    s.sendall(f"{mode} {word}\n".encode())
    data = b''
    while True:
        part = s.recv(1024)
        if not part:
            break
        data += part
    s.close()
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
root.title("Centered trial 1")
root.geometry("400x300")

# Heading
heading = Label(
    root,
    text="My First try at a notepad with autocomplete suggestions",
    font=("Helvetica", 19),
    fg="black",
    bg="white"
)
heading.pack(padx=20, pady=(30, 10))

# Textbox
textbox = Text(
    root,
    width=80,
    height=10,
    fg="black",
    bg="lightblue"
)
textbox.pack(padx=30, pady=(10, 5))
textbox.bind("<KeyRelease>", on_key_release)
textbox.bind("<space>", on_space)

# Listbox for autocomplete suggestions
listbox = Listbox(root, height=4)
listbox.pack(padx=30, pady=(0, 10))

root.mainloop()
