import tkinter as tk
from tkinter import messagebox
import string
import random

class LockForge:
    def __init__(self, length=16, useUpper=True, useDigits=True, useSymbols=True):
        self.length = length
        self.useUpper = useUpper
        self.useDigits = useDigits
        self.useSymbols = useSymbols

    def generatePassword(self):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase if self.useUpper else ''
        digits = string.digits if self.useDigits else ''
        symbols = string.punctuation if self.useSymbols else ''

        allChars = lower + upper + digits + symbols

        if not allChars:
            raise ValueError("Select at least one character type!")

        password = []
        if self.useUpper:
            password.append(random.choice(upper))
        if self.useDigits:
            password.append(random.choice(digits))
        if self.useSymbols:
            password.append(random.choice(symbols))
        password.append(random.choice(lower))

        remaining = self.length - len(password)
        password += random.choices(allChars, k=remaining)

        random.shuffle(password)
        return ''.join(password)

# Store passwords in memory
savedPasswords = []

def savePassword():
    password = resultEntry.get()
    description = descEntry.get().strip()

    if not password:
        messagebox.showwarning("No Password", "Please generate a password first!")
        return
    if not description:
        messagebox.showwarning("Missing Description", "Please enter a description for the password.")
        return

    savedPasswords.append({"description": description, "password": password})
    messagebox.showinfo("Saved", f"Password saved with description: {description}")
    descEntry.delete(0, tk.END)

def copyToClipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def deletePassword(index, window):
    del savedPasswords[index]
    window.destroy()
    viewSaved()

def viewSaved():
    if not savedPasswords:
        messagebox.showinfo("Saved Passwords", "No passwords saved yet.")
        return

    viewWindow = tk.Toplevel(root)
    viewWindow.title("Saved Passwords")
    viewWindow.geometry("450x300")
    viewWindow.resizable(False, False)

    tk.Label(viewWindow, text="Saved Passwords", font=("Helvetica", 14, "bold")).pack(pady=10)

    frame = tk.Frame(viewWindow)
    frame.pack(fill='both', expand=True, padx=10, pady=5)

    for idx, item in enumerate(savedPasswords):
        desc = item['description']
        pwd = item['password']

        tk.Label(frame, text=f"{idx + 1}. {desc}", anchor='w').grid(row=idx, column=0, sticky='w')
        tk.Button(frame, text="Copy", command=lambda p=pwd: copyToClipboard(p)).grid(row=idx, column=1, padx=5)
        tk.Button(frame, text="Delete", command=lambda i=idx: deletePassword(i, viewWindow)).grid(row=idx, column=2, padx=5)

def generate():
    try:
        length = int(lengthEntry.get())
        useUpper = upperVar.get()
        useDigits = digitVar.get()
        useSymbols = symbolVar.get()

        lockforge = LockForge(length, useUpper, useDigits, useSymbols)
        password = lockforge.generatePassword()
        resultEntry.delete(0, tk.END)
        resultEntry.insert(0, password)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Main Window
root = tk.Tk()
root.title("🔐 LockForge Password Generator")
root.geometry("420x460")
root.resizable(False, False)

tk.Label(root, text="LockForge", font=("Helvetica", 18, "bold")).pack(pady=10)
tk.Label(root, text="Password Length:").pack()

lengthEntry = tk.Entry(root)
lengthEntry.insert(0, "16")
lengthEntry.pack(pady=5)

upperVar = tk.BooleanVar(value=True)
digitVar = tk.BooleanVar(value=True)
symbolVar = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase Letters", variable=upperVar).pack(anchor='w', padx=40)
tk.Checkbutton(root, text="Include Digits", variable=digitVar).pack(anchor='w', padx=40)
tk.Checkbutton(root, text="Include Symbols", variable=symbolVar).pack(anchor='w', padx=40)

tk.Button(root, text="Generate Password", command=generate, bg="#4CAF50", fg="white").pack(pady=10)

resultEntry = tk.Entry(root, width=40, font=("Courier", 12), justify='center')
resultEntry.pack(pady=5)

tk.Label(root, text="Password Description (e.g. Gmail, Facebook):").pack(pady=(10, 0))
descEntry = tk.Entry(root, width=40)
descEntry.pack(pady=5)

tk.Button(root, text="Save Password", command=savePassword, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="View Saved Passwords", command=viewSaved, bg="#9C27B0", fg="white").pack(pady=5)

root.mainloop()