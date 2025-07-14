# ✨ Typright — The Smartest Local Notepad

> A blazing fast **offline** notepad with **real-time spell check** and **autocomplete** — built with Python (Tkinter frontend) and a C++ backend server. Designed for speed, precision, and privacy.

---

## 🚀 Features

- 🧠 **Smart Autocomplete** using Trie data structures  
- 🛠️ **Real-time Spell Checking** using Levenshtein distance  
- 💾 **Save/Load Files** in `.txt`, `.md`, `.log`, and custom extensions  
- 🔒 **Works Offline** – No internet dependency    
- 🎯 Minimal, fast, distraction-free UI

---

## 🖼️ Preview

> _(Screenshot coming soon)_

---

## 🛠️ Architecture

```mermaid
flowchart LR
    A[User Typing in UI] --> B[Python Frontend (Tkinter)]
    B -->|Sends request| C[Local Python Client Socket]
    C -->|Text + Mode| D[C++ Backend Server]
    D -->|Suggestions| C
    C -->|Return words| B
```

---

## 🧰 Tech Stack

| Layer        | Technology                 |
|-------------|----------------------------|
| UI          | Python + Tkinter           |
| Frontend    | Python socket client       |
| Backend     | C++ (Spell check + Trie)   |
| Communication | Localhost TCP Socket     |

---

## 📂 Project Structure

```
typright/
├── wordlist.txt              # Dictionary for spellcheck & autocomplete
├── gui.py                 # Frontend logic (Tkinter + Socket)
├── server.cpp                # C++ server (Trie + Levenshtein)
├── tries_trial.cpp/.h             # Trie implementation
├── README.md
```

---

## 🔧 How to Run

### Prerequisites

- Python 3.x  
- g++ or any C++ compiler  
- WSL (Linux recommended for easier socket handling)

---

### Step 1: Compile the C++ Server

```bash
g++ server.cpp tries.cpp levenshtein.cpp -o server
./server
```

### Step 2: Launch the Python Frontend

```bash
python3 client.py
```

---

## 🌐 Modes of Operation

- `auto word` → Suggest autocomplete words  
- `spell word` → Suggest corrected spellings  

---

## 💡 Example

```txt
Input: spell tryp
Suggestions: try, trip, type, trap, tryout
```

---

## 🧠 How It Works

- **Autocomplete**:  
  Uses a Trie structure to fetch prefix-matching words in `O(k)` time.

- **Spell Check**:  
  Uses Levenshtein distance to find words with minimal edits.

- **Socket Communication**:  
  Python sends request strings like `spell helloo`, C++ parses and returns top 5 closest matches.

---

## 📈 Future Improvements

- [ ] Add theme switcher (Dark/Light)  
- [ ] Support grammar suggestions  
- [ ] Export as `.pdf`  
- [ ] Add right-click context menu  

---
