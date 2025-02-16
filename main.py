import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
from newstego import load_image, encode_message, decode_message, save_image

# Define color variables
bg_color = "#EEDFD3" #violrt
button_color = "#FAD0AF"   
text_color = "#4A4937"    
entry_bg = "#D2ADBD"
entry_fg = "#4A4937"     

def select_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        image_path_var.set(file_path)

def encrypt():
    image_path = image_path_var.get()
    secret_msg = message_entry.get()
    passcode = passcode_entry.get()
    
    if not image_path or not secret_msg or not passcode:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        img = load_image(image_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    try:
        encoded_img = encode_message(img, secret_msg)
    except Exception as e:
        messagebox.showerror("Error", f"Error encoding message: {e}")
        return

    # Save as PNG for lossless compression
    encrypted_image_path = "encryptedImage.png"
    save_image(encoded_img, encrypted_image_path)
    messagebox.showinfo("Success", f"Encryption is complete!\nSaved as {encrypted_image_path}")
    
    # Enable the decrypt button after encryption is complete
    decrypt_button.config(state="normal")

def decrypt():
    entered_passcode = decrypt_passcode_entry.get()
    # Check if the entered decryption passcode matches the encryption passcode
    if entered_passcode != passcode_entry.get():
        messagebox.showerror("Error", "Incorrect passcode!")
        return

    encrypted_image_path = "encryptedImage.png"
    try:
        img = load_image(encrypted_image_path)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    # Use the original message length to decode the message
    secret_msg = message_entry.get()
    try:
        decrypted_message = decode_message(img, len(secret_msg))
    except Exception as e:
        messagebox.showerror("Error", f"Error decoding message: {e}")
        return

    messagebox.showinfo("Decrypted Message", f"Message: {decrypted_message}")

# Create the main window
root = tk.Tk()
root.title("Stego")
root.configure(bg=bg_color)

# Variable to hold the image path
image_path_var = tk.StringVar()

# Select Image Button and Label
select_image_button = tk.Button(root, text="Select Image", command=select_image, bg=button_color, fg="black")
select_image_button.grid(row=0, column=0, padx=10, pady=10)

image_path_label = tk.Label(root, textvariable=image_path_var, bg=bg_color, fg=text_color)
image_path_label.grid(row=0, column=1, padx=10, pady=10)

# Secret Message Entry
secret_msg_label = tk.Label(root, text="Secret Message:", bg=bg_color, fg=text_color)
secret_msg_label.grid(row=1, column=0, padx=10, pady=10)

message_entry = tk.Entry(root, width=40, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
message_entry.grid(row=1, column=1, padx=10, pady=10)

# Passcode for Encryption
passcode_label = tk.Label(root, text="Passcode:", bg=bg_color, fg=text_color)
passcode_label.grid(row=2, column=0, padx=10, pady=10)

passcode_entry = tk.Entry(root, show="*", width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
passcode_entry.grid(row=2, column=1, padx=10, pady=10)

# Encrypt Button
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt, bg=button_color, fg="black")
encrypt_button.grid(row=3, column=0, padx=10, pady=10)

# Decryption Passcode Entry
decrypt_passcode_label = tk.Label(root, text="Enter Passcode for Decryption:", bg=bg_color, fg=text_color)
decrypt_passcode_label.grid(row=4, column=0, padx=10, pady=10)

decrypt_passcode_entry = tk.Entry(root, show="*", width=20, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
decrypt_passcode_entry.grid(row=4, column=1, padx=10, pady=10)

# Decrypt Button (initially disabled)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt, bg=button_color, fg="black", state="disabled")
decrypt_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
