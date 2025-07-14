Frontend (Python Tkinter GUI)

Handles user input (text box)

Detects key events

Sends requests to the server over a socket

Displays suggestions and highlights spelling errors

Backend (C++ server)

Loads a dictionary (wordlist.txt) into a Trie

Listens for TCP socket connections on port 4000

Accepts requests like autocomplete word or spellcheck word

Returns results as newline-separated suggestions