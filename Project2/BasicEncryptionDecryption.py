import tkinter as tk
from tkinter import messagebox

def encrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + shift) % 26 + start)
        else:
            result += char

    return result


def decrypt(text, shift):
    return encrypt(text, -shift)

def encrypt_text():
    try:
        text = text_entry.get()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text.")
            return

        shift = int(shift_entry.get())

        encrypted = encrypt(text, shift)

        encrypted_output.config(state="normal")
        encrypted_output.delete(0, tk.END)
        encrypted_output.insert(0, encrypted)
        encrypted_output.config(state="readonly")

    except ValueError:
        messagebox.showerror("Error", "Shift key must be a number.")


def decrypt_text():
    try:
        encrypted_text = encrypted_output.get()

        if not encrypted_text:
            messagebox.showwarning("Warning", "Please encrypt text first.")
            return

        shift = int(shift_entry.get())

        decrypted = decrypt(encrypted_text, shift)

        decrypted_output.config(state="normal")
        decrypted_output.delete(0, tk.END)
        decrypted_output.insert(0, decrypted)
        decrypted_output.config(state="readonly")

    except ValueError:
        messagebox.showerror("Error", "Shift key must be a number.")


def clear_all():
    text_entry.delete(0, tk.END)
    shift_entry.delete(0, tk.END)
    shift_entry.insert(0, "3")

    encrypted_output.config(state="normal")
    encrypted_output.delete(0, tk.END)
    encrypted_output.config(state="readonly")

    decrypted_output.config(state="normal")
    decrypted_output.delete(0, tk.END)
    decrypted_output.config(state="readonly")

root = tk.Tk()
root.title("Cyber Security - Basic Encryption & Decryption")
root.geometry("650x450")
root.resizable(False, False)

BG_COLOR = "#0A0F0D"
FG_COLOR = "#00FF41"
ENTRY_BG = "#111111"  
BTN_BG = "#1B1B1B"
OUTPUT_COLOR = "#111111"

root.configure(bg=BG_COLOR)


title_label = tk.Label(
    root,
    text="CYBER SECURITY ENCRYPTION & DECRYPTION",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 16, "bold")
)
title_label.pack(pady=15)

input_label = tk.Label(
    root,
    text="Enter Text",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 11)
)
input_label.pack()

text_entry = tk.Entry(
    root,
    width=60,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    font=("Consolas", 11)
)
text_entry.pack(pady=8)

shift_label = tk.Label(
    root,
    text="Shift Key",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 11)
)
shift_label.pack()

shift_entry = tk.Entry(
    root,
    width=10,
    bg=ENTRY_BG,
    fg=FG_COLOR,
    insertbackground=FG_COLOR,
    justify="center",
    font=("Consolas", 11)
)
shift_entry.pack(pady=8)
shift_entry.insert(0, "3")

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=15)

encrypt_btn = tk.Button(
    button_frame,
    text="Encrypt",
    width=15,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground="#003300",
    activeforeground="white",
    font=("Consolas", 10, "bold"),
    command=encrypt_text
)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(
    button_frame,
    text="Decrypt",
    width=15,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground="#003300",
    activeforeground="white",
    font=("Consolas", 10, "bold"),
    command=decrypt_text
)
decrypt_btn.grid(row=0, column=1, padx=10)

clear_btn = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    bg=BTN_BG,
    fg=FG_COLOR,
    activebackground="#330000",
    activeforeground="white",
    font=("Consolas", 10, "bold"),
    command=clear_all
)
clear_btn.grid(row=0, column=2, padx=10)

encrypted_label = tk.Label(
    root,
    text="Encrypted Text",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 11)
)
encrypted_label.pack()

encrypted_output = tk.Entry(
    root,
    width=60,
    font=("Consolas", 11, "bold"),
    bg=ENTRY_BG,
    fg=OUTPUT_COLOR,
    state="readonly"
)
encrypted_output.pack(pady=8)

decrypted_label = tk.Label(
    root,
    text="Decrypted Text",
    bg=BG_COLOR,
    fg=FG_COLOR,
    font=("Consolas", 11, "bold")
)
decrypted_label.pack()

decrypted_output = tk.Entry(
    root,
    width=60,
    font=("Consolas", 11, "bold"),
    bg=ENTRY_BG,
    fg=OUTPUT_COLOR,
    state="readonly"
)
decrypted_output.pack(pady=8)

footer = tk.Label(
    root,
    text="DecodeLabs Cyber Security Project 2",
    bg=BG_COLOR,
    fg="#888888",
    font=("Consolas", 9)
)
footer.pack(side="bottom", pady=15)

root.mainloop()