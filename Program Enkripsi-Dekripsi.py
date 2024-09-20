import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

def vigenere_encrypt(plaintext, key):
    key = key.lower()
    encrypted = ""
    key_index = 0
    for char in plaintext.lower():
        if char.isalpha():
            shift = ord(key[key_index]) - ord('a')
            encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            key_index = (key_index + 1) % len(key)
        else:
            encrypted += char
    return encrypted

def vigenere_decrypt(ciphertext, key):
    key = key.lower()
    decrypted = ""
    key_index = 0
    for char in ciphertext.lower():
        if char.isalpha():
            shift = ord(key[key_index]) - ord('a')
            decrypted += chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a'))
            key_index = (key_index + 1) % len(key)
        else:
            decrypted += char
    return decrypted

def generate_playfair_matrix(key):
    matrix = []
    key = ''.join(sorted(set(key), key=lambda k: key.index(k))) 
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    for char in key:
        if char not in matrix and char in alphabet:
            matrix.append(char)
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def playfair_encrypt(plaintext, key):
    plaintext = plaintext.replace("j", "i").replace(" ", "")
    if len(plaintext) % 2 != 0:
        plaintext += "x"  
    matrix = generate_playfair_matrix(key)
    
    encrypted = ""
    for i in range(0, len(plaintext), 2):
        char1, char2 = plaintext[i], plaintext[i+1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            encrypted += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            encrypted += matrix[row1][col2] + matrix[row2][col1]
    
    return encrypted

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    
    decrypted = ""
    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i+1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            decrypted += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            decrypted += matrix[row1][col2] + matrix[row2][col1]
    
    return decrypted

def hill_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").lower()
    if len(plaintext) % len(key) != 0:
        plaintext += 'x' * (len(key) - len(plaintext) % len(key))  
    
    matrix_key = np.array(key)
    n = len(key)
    
    encrypted = ""
    for i in range(0, len(plaintext), n):
        vector = [ord(char) - ord('a') for char in plaintext[i:i+n]]
        encrypted_vector = np.dot(matrix_key, vector) % 26
        encrypted += ''.join([chr(num + ord('a')) for num in encrypted_vector])
    
    return encrypted

def hill_decrypt(ciphertext, key):
    matrix_key = np.array(key)
    matrix_key_inv = np.linalg.inv(matrix_key).astype(int) % 26 
    
    decrypted = ""
    for i in range(0, len(ciphertext), len(key)):
        vector = [ord(char) - ord('a') for char in ciphertext[i:i+len(key)]]
        decrypted_vector = np.dot(matrix_key_inv, vector) % 26
        decrypted += ''.join([chr(num + ord('a')) for num in decrypted_vector])
    
    return decrypted

def open_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                input_text.delete(1.0, tk.END)
                input_text.insert(tk.END, content)
    except Exception as e:
        messagebox.showerror("Error", f"tidak dapat membuka file (pilih file .txt): {e}")

def process_text():
    cipher_type = cipher_method.get()
    mode = operation.get()
    key = key_entry.get().strip()
    
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci minimal harus 12 karakter!")
        return
    
    plaintext = input_text.get(1.0, tk.END).strip()
    if not plaintext:
        messagebox.showerror("Error", "input text tidak dapat kosong!")
        return

    try:
        if cipher_type == "Vigenere":
            if mode == "Encrypt":
                result = vigenere_encrypt(plaintext, key)
            else:
                result = vigenere_decrypt(plaintext, key)
        
        elif cipher_type == "Playfair":
            if mode == "Encrypt":
                result = playfair_encrypt(plaintext, key)
            else:
                result = playfair_decrypt(plaintext, key)
        
        elif cipher_type == "Hill":
            if mode == "Encrypt":
                result = hill_encrypt(plaintext, key)
            else:
                result = hill_decrypt(plaintext, key)

        result_output.delete(1.0, tk.END)
        result_output.insert(tk.END, result)

    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

root = tk.Tk()
root.title("Program Enkripsi dan Dekripsi")
root.geometry("500x400")
root.config(bg="#f0f8ff")
label_font = ("Helvetica", 12)
entry_font = ("Helvetica", 11)
button_font = ("Helvetica", 10, "bold")

input_label = tk.Label(root, text="Input Text:", font=label_font, bg="#f0f8ff")
input_label.pack(pady=5)
input_text = tk.Text(root, height=5, width=50, font=entry_font)
input_text.pack(pady=5)

open_file_button = tk.Button(root, text="Open File", command=open_file, bg="#4682b4", fg="white", font=button_font)
open_file_button.pack(pady=5)

key_label = tk.Label(root, text="Masukkan kunci (minimal 12 karakter):", font=label_font, bg="#f0f8ff")
key_label.pack(pady=5)
key_entry = tk.Entry(root, width=30, font=entry_font)
key_entry.pack(pady=5)

cipher_method = tk.StringVar(value="Vigenere")
method_label = tk.Label(root, text="Pilih Metode:", font=label_font, bg="#f0f8ff")
method_label.pack(pady=5)
method_menu = tk.OptionMenu(root, cipher_method, "Vigenere", "Playfair", "Hill")
method_menu.config(bg="#4682b4", fg="white", font=button_font)
method_menu.pack(pady=5)

operation = tk.StringVar(value="Encrypt")
operation_menu = tk.OptionMenu(root, operation, "Encrypt", "Decrypt")
operation_menu.config(bg="#4682b4", fg="white", font=button_font)
operation_menu.pack(pady=5)

process_button = tk.Button(root, text="Start", command=process_text, bg="#32cd32", fg="white", font=button_font)
process_button.pack(pady=10)

result_label = tk.Label(root, text="Output Text:", font=label_font, bg="#f0f8ff")
result_label.pack(pady=5)
result_output = tk.Text(root, height=5, width=50, font=entry_font)
result_output.pack(pady=5)

root.mainloop()
