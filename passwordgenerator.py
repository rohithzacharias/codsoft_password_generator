import customtkinter as ctk
import random
import string
import pyperclip

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App setup
app = ctk.CTk()
app.title("Password Generator & Checker")
app.geometry("440x680")
app.resizable(False, False)

# Variables
length_var = ctk.IntVar(value=12)
uppercase_var = ctk.BooleanVar(value=True)
lowercase_var = ctk.BooleanVar(value=True)
numbers_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)
password_var = ctk.StringVar()
strength_stars_var = ctk.StringVar()
length_label_var = ctk.StringVar(value="Password Length: 12")
custom_password_var = ctk.StringVar()
custom_stars_var = ctk.StringVar()
custom_feedback_var = ctk.StringVar()

# Update length label dynamically
def update_length_label(value):
    length_label_var.set(f"Password Length: {int(float(value))}")

# Increase/Decrease slider
def increase_length():
    if length_var.get() < 32:
        length_var.set(length_var.get() + 1)
        update_length_label(length_var.get())

def decrease_length():
    if length_var.get() > 6:
        length_var.set(length_var.get() - 1)
        update_length_label(length_var.get())

# Password generation logic
def generate_password():
    chars = ""
    if uppercase_var.get():
        chars += string.ascii_uppercase
    if lowercase_var.get():
        chars += string.ascii_lowercase
    if numbers_var.get():
        chars += string.digits
    if symbols_var.get():
        chars += string.punctuation

    if not chars:
        password_var.set("Select at least one option")
        strength_stars_var.set("--")
        return

    length = length_var.get()
    password = ''.join(random.choice(chars) for _ in range(length))
    password_var.set(password)
    update_strength(password, strength_stars_var, custom_feedback_var)

# Strength checker with star ratings
def update_strength(pw, star_output_var, feedback_output_var=None):
    length = len(pw)
    score = 0
    feedback = []

    if any(c.islower() for c in pw):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c.isupper() for c in pw):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c.isdigit() for c in pw):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(c in string.punctuation for c in pw):
        score += 1
    else:
        feedback.append("Add special characters")

    if length >= 12:
        score += 1
    else:
        feedback.append("Use at least 12 characters")

    stars = ""
    if score == 5:
        stars = "★★★★★"
        if feedback_output_var is not None:
            feedback_output_var.set("Your Password is Strong")
    elif score == 4:
        stars = "★★★★"
        if feedback_output_var is not None:
            feedback_output_var.set("Suggestions: " + ", ".join(feedback))
    elif score == 3:
        stars = "★★★"
        if feedback_output_var is not None:
            feedback_output_var.set("Suggestions: " + ", ".join(feedback))
    elif score == 2:
        stars = "★★"
        if feedback_output_var is not None:
            feedback_output_var.set("Suggestions: " + ", ".join(feedback))
    else:
        stars = "★"
        if feedback_output_var is not None:
            feedback_output_var.set("Suggestions: " + ", ".join(feedback))

    star_output_var.set(stars)

# Copy to clipboard
def copy_to_clipboard():
    pw = password_var.get()
    if pw and "Select" not in pw:
        pyperclip.copy(pw)
        ctk.CTkLabel(app, text="Copied!", text_color="green").pack()

# Custom password checker
def check_custom_password():
    pw = custom_password_var.get()
    if pw:
        update_strength(pw, custom_stars_var, custom_feedback_var)
    else:
        custom_stars_var.set("Enter a password")
        custom_feedback_var.set("")

# UI layout
ctk.CTkLabel(app, textvariable=length_label_var, font=("Arial", 16)).pack(pady=10)

length_frame = ctk.CTkFrame(app)
length_frame.pack(pady=5)
ctk.CTkButton(length_frame, text="←", width=40, command=decrease_length).pack(side="left", padx=5)
ctk.CTkSlider(length_frame, from_=6, to=32, variable=length_var, command=update_length_label, number_of_steps=26, width=200).pack(side="left")
ctk.CTkButton(length_frame, text="→", width=40, command=increase_length).pack(side="left", padx=5)

# Options
for text, var in [
    ("Include Uppercase Letters", uppercase_var),
    ("Include Lowercase Letters", lowercase_var),
    ("Include Numbers", numbers_var),
    ("Include Symbols", symbols_var),
]:
    ctk.CTkCheckBox(app, text=text, variable=var).pack(anchor="w", padx=20, pady=5)

ctk.CTkButton(app, text="Generate Password", command=generate_password).pack(pady=10)
ctk.CTkEntry(app, textvariable=password_var, font=("Arial", 16), width=300).pack(pady=5)
ctk.CTkButton(app, text="Copy to Clipboard", command=copy_to_clipboard).pack()
ctk.CTkLabel(app, textvariable=strength_stars_var, font=("Arial", 18)).pack(pady=5)

# Custom password checker
ctk.CTkLabel(app, text="\nCheck Your Own Password:", font=("Arial", 16)).pack(pady=5)
ctk.CTkEntry(app, textvariable=custom_password_var, font=("Arial", 14), width=300).pack(pady=5)
ctk.CTkButton(app, text="Check Strength", command=check_custom_password).pack(pady=5)
ctk.CTkLabel(app, textvariable=custom_stars_var, font=("Arial", 18)).pack()
ctk.CTkLabel(app, textvariable=custom_feedback_var, font=("Arial", 12), wraplength=350, text_color="orange").pack(pady=5)

app.mainloop()