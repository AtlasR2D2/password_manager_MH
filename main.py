import tkinter as tk
from tkinter import messagebox
from pwd_gen import random_pwd
import pyperclip
import json

PADLOCK_ICON = "\U0001F512"
HEIGHT_AMOUNT = 200
WIDTH_AMOUNT = 200
PADDING_AMOUNT = 20
DELIMITER = "|"
DEFAULT_EMAIL = "abc@def.com"
WEAK_LENGTH = 50
MEDIUM_LENGTH = 100
STRONG_LENGTH = 200
MIN_PWD_LENGTH = 6
pwd_length = 0
strPassword = ""
lowercase_count = 0
uppercase_count = 0
number_count = 0
symbol_count = 0

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_random_password():
    random_password = random_pwd()
    pyperclip.copy(random_password)
    password_sv.set(random_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def pwd_strength(key):
    global pwd_length, strPassword
    entered_password = strPassword
    pwd_length = len(entered_password)
    lowercase_count = 0
    uppercase_count = 0
    number_count = 0
    symbol_count = 0
    for char in entered_password:
        if char.isnumeric():
            number_count += 1
        elif not char.isalpha():
            symbol_count += 1
        elif char.lower() == char:
            lowercase_count += 1
        elif char.upper() == char:
            uppercase_count += 1

    if pwd_length >= MIN_PWD_LENGTH and (lowercase_count > 0 and uppercase_count > 0) and (number_count > 0 and symbol_count > 0):
        strength = "STRONG"
    elif pwd_length >= MIN_PWD_LENGTH and (lowercase_count > 0 and uppercase_count > 0) and (number_count > 0 or symbol_count > 0):
        strength = "MEDIUM"
    else:
        strength = "WEAK"
    # Set Password Bar
    if strength == "STRONG":
        set_length = STRONG_LENGTH
        set_color = "green"
    elif strength == "MEDIUM":
        set_length = MEDIUM_LENGTH
        set_color = "orange"
    elif strength == "WEAK":
        set_length = WEAK_LENGTH
        set_color = "red"
    else:
        set_length = WEAK_LENGTH
        set_color = "red"
    # Apply formatting to Password Bar
    orig_coords = canvas_pwd.coords(pwd_bar)
    orig_coords[2] = set_length
    canvas_pwd.coords(pwd_bar, orig_coords)
    canvas_pwd.itemconfig(pwd_bar, fill=set_color)


def save_password():
    global DELIMITER
    strWebsite = entryWebsite.get().title()
    strLogin = entryLogin.get()
    strPassword = entryPwd.get()

    # Check for blank entry fields
    if len(strPassword) == 0 or len(strWebsite) == 0 or len(strLogin) == 0:
        messagebox.showerror(title=f"{PADLOCK_ICON} Password Manager", message="Don't leave any fields empty!")
    else:
        # Proceed with save attempt
        password_details = [strWebsite, strLogin, strPassword]
        password_details_string = DELIMITER.join(password_details)
        password_details_json = {
            strWebsite: {
                "Login": strLogin,
                "Password": strPassword
            }
        }

        # Ask user to confirm save attempt
        q_ans = messagebox.askyesno(title=f"{PADLOCK_ICON} Password Manager", \
                            message=f"Are you sure you want to add these details?\n{password_details_string}")
        if q_ans:
            # Proceed with save
            try:
                with open("password_manager.json", "r") as file:
                    # Read old data
                    data = json.load(file)
                    # Update data
                    data.update(password_details_json)
            except json.JSONDecodeError:
                data = password_details_json
            except FileNotFoundError:
                data = password_details_json
            finally:
                with open("password_manager.json", "w") as file:
                    json.dump(data, file, indent=4)

                # file.write(password_details_string+"\n")
            #Clear inputs
            entryWebsite.delete(0, tk.END)
            entryPwd.delete(0, tk.END)
            # Only clear login entry if a default email is not specified
            if len(DEFAULT_EMAIL) == 0:
                entryLogin.delete(0, tk.END)
# ---------------------------- RETRIEVE PASSWORD ------------------------------- #


def retrieve_details():
    search_field = entryWebsite.get().title()
    try:
        with open("password_manager.json", "r") as file:
            password_manager_data = json.load(file)
            try:
                password_details = password_manager_data[search_field]
            except KeyError:
                messagebox.showerror(title=f"{PADLOCK_ICON} Password Manager", \
                                     message="An entry has not been added for this website!")
            else:
                messagebox.showinfo(title=f"{PADLOCK_ICON} Password Manager", \
                                    message=f"Website: {search_field}\nLogin: {password_details['Login']}\nPassword: {password_details['Password']}")
    except FileNotFoundError:
        messagebox.showerror(title=f"{PADLOCK_ICON} Password Manager", \
                             message="Password Manager file can't be found!")

# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()

window.title(f"{PADLOCK_ICON} Password Manager")
window.config(padx=PADDING_AMOUNT, pady=PADDING_AMOUNT)
# Canvas
# -----------------------------------------
# Padlock
canvas = tk.Canvas(width=WIDTH_AMOUNT, height=HEIGHT_AMOUNT)
padlock_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(row=0, column=1)
# -----------------------------------------
# Password Strength
canvas_pwd = tk.Canvas(width=200, height=10)
pwd_bar = canvas_pwd.create_rectangle(0, 0, 200, 10, fill="red")
canvas_pwd.grid(row=4, column=1, columnspan=2, sticky="w")
# -----------------------------------------

# Labels
# -----------------------------------------
lblWebsite = tk.Label(text="Website:")
lblWebsite.grid(column=0, row=1, padx=10, pady=10)
# -----------------------------------------
lblLogin = tk.Label(text="Email/Website:")
lblLogin.grid(column=0, row=2, padx=10, pady=10)
# -----------------------------------------
lblPwd = tk.Label(text="Password:")
lblPwd.grid(column=0, row=3, padx=10, pady=10)
# -----------------------------------------
# Entry Boxes
# -----------------------------------------
entryWebsite = tk.Entry(width=35)
entryWebsite.grid(column=1, row=1, sticky="W")
# -----------------------------------------
entryLogin = tk.Entry(width=35)
entryLogin.insert(0,DEFAULT_EMAIL)
entryLogin.grid(column=1, row=2, columnspan=2, sticky="W")
# -----------------------------------------


def set_pwd(var):
    global strPassword
    strPassword = var.get()
    pwd_strength(var)
    # print(strPassword)


password_sv = tk.StringVar()
password_sv.trace('w', lambda nm, idx, mode, var=password_sv: set_pwd(var))
entryPwd = tk.Entry(window, width=21, textvariable=password_sv)
entryPwd.grid(column=1, row=3, columnspan=2, sticky="W")
entryPwd.bind("<Key>", pwd_strength)
# Buttons
# -----------------------------------------
buttonGenPwd = tk.Button(text="Generate Password", command=generate_random_password)
buttonGenPwd.grid(column=2, row=3)
# -----------------------------------------
buttonAdd = tk.Button(text="Add", width=36, command=save_password)
buttonAdd.grid(column=1, row=5, columnspan=2, sticky="W")
# -----------------------------------------
buttonRetrieve = tk.Button(text="Retrieve Details", command=retrieve_details)
buttonRetrieve.grid(column=2, row=1, sticky="W")


# Set focus to first entry box
entryWebsite.focus_set()

window.mainloop()
