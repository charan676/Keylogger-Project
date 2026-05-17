import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
from datetime import datetime
import json

# ==========================================
# FILE NAMES
# ==========================================

TEXT_LOG_FILE = "key_log.txt"
JSON_LOG_FILE = "key_log.json"

# ==========================================
# GLOBAL VARIABLES
# ==========================================

listener = None
keys_used = []
is_logging = False

# ==========================================
# SAVE TEXT LOG
# ==========================================

def generate_text_log(text):

    try:

        with open(TEXT_LOG_FILE, "a", encoding="utf-8") as file:

            file.write(text)

            file.flush()

    except Exception as error:

        messagebox.showerror(
            "Text Log Error",
            f"Unable to save text log.\n{error}"
        )

# ==========================================
# SAVE JSON LOG
# ==========================================

def generate_json_log():

    try:

        with open(JSON_LOG_FILE, "w", encoding="utf-8") as file:

            json.dump(
                keys_used,
                file,
                indent=4
            )

    except Exception as error:

        messagebox.showerror(
            "JSON Error",
            f"Unable to save JSON log.\n{error}"
        )

# ==========================================
# FORMAT SPECIAL KEYS
# ==========================================

def format_key(key):

    try:

        if key.char is not None:

            return key.char

    except AttributeError:

        pass

    special_keys = {

        keyboard.Key.space: " ",

        keyboard.Key.enter: "\n",

        keyboard.Key.tab: "[TAB]",

        keyboard.Key.backspace: "[BACKSPACE]",

        keyboard.Key.shift: "[SHIFT]",

        keyboard.Key.shift_r: "[SHIFT]",

        keyboard.Key.ctrl_l: "[CTRL]",

        keyboard.Key.ctrl_r: "[CTRL]",

        keyboard.Key.alt_l: "[ALT]",

        keyboard.Key.alt_r: "[ALT]",

        keyboard.Key.caps_lock: "[CAPSLOCK]",

        keyboard.Key.esc: "[ESC]",

        keyboard.Key.delete: "[DELETE]"
    }

    return special_keys.get(
        key,
        f"[{key}]"
    )

# ==========================================
# KEY PRESS EVENT
# ==========================================

def on_press(key):

    global keys_used

    formatted_key = format_key(key)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Save clean JSON log
    keys_used.append({

        "key": formatted_key,

        "time": timestamp
    })

    generate_json_log()

    # Save clean text log
    generate_text_log(formatted_key)

# ==========================================
# START KEYLOGGER
# ==========================================

def start_keylogger():

    global listener
    global is_logging

    if not is_logging:

        listener = keyboard.Listener(

            on_press=on_press
        )

        listener.start()

        is_logging = True

        status_label.config(

            text="[+] Keyboard Monitoring Started",

            fg="#00ff88"
        )

        start_button.config(state="disabled")

        stop_button.config(state="normal")

# ==========================================
# STOP KEYLOGGER
# ==========================================

def stop_keylogger():

    global listener
    global is_logging

    if listener:

        listener.stop()

        is_logging = False

        status_label.config(

            text="[!] Keyboard Monitoring Stopped",

            fg="#ff5555"
        )

        start_button.config(state="normal")

        stop_button.config(state="disabled")

# ==========================================
# CLEAR LOGS
# ==========================================

def clear_logs():

    global keys_used

    keys_used = []

    try:

        open(TEXT_LOG_FILE, "w").close()

        with open(JSON_LOG_FILE, "w") as file:

            json.dump([], file)

        messagebox.showinfo(

            "Logs Cleared",

            "All logs cleared successfully."
        )

    except Exception as error:

        messagebox.showerror(

            "Clear Error",

            f"Unable to clear logs.\n{error}"
        )

# ==========================================
# SHOW LOGS
# ==========================================

def show_logs():

    try:

        with open(TEXT_LOG_FILE, "r", encoding="utf-8") as file:

            content = file.read()

        log_window = tk.Toplevel(root)

        log_window.title("Saved Logs")

        log_window.geometry("500x400")

        text_area = tk.Text(

            log_window,

            bg="#1e1e1e",

            fg="white",

            font=("Consolas", 10)
        )

        text_area.pack(fill="both", expand=True)

        text_area.insert("1.0", content)

    except FileNotFoundError:

        messagebox.showwarning(

            "No Logs",

            "No log file found."
        )

# ==========================================
# EXIT APPLICATION
# ==========================================

def exit_application():

    stop_keylogger()

    root.destroy()

# ==========================================
# GUI WINDOW
# ==========================================

root = tk.Tk()

root.title("Keyboard Activity Monitor")

root.geometry("500x420")

root.configure(bg="#121212")

root.resizable(False, False)

# ==========================================
# TITLE LABEL
# ==========================================

title_label = tk.Label(

    root,

    text="Keyboard Activity Monitor",

    font=("Arial", 18, "bold"),

    bg="#121212",

    fg="white"
)

title_label.pack(pady=20)

# ==========================================
# STATUS LABEL
# ==========================================

status_label = tk.Label(

    root,

    text="Click START to Begin Monitoring",

    font=("Arial", 11),

    bg="#121212",

    fg="white"
)

status_label.pack(pady=10)

# ==========================================
# BUTTON FRAME
# ==========================================

button_frame = tk.Frame(

    root,

    bg="#121212"
)

button_frame.pack(pady=20)

# ==========================================
# START BUTTON
# ==========================================

start_button = tk.Button(

    button_frame,

    text="START",

    width=12,

    height=2,

    bg="#00aa55",

    fg="white",

    font=("Arial", 10, "bold"),

    command=start_keylogger
)

start_button.grid(row=0, column=0, padx=10)

# ==========================================
# STOP BUTTON
# ==========================================

stop_button = tk.Button(

    button_frame,

    text="STOP",

    width=12,

    height=2,

    bg="#cc3333",

    fg="white",

    font=("Arial", 10, "bold"),

    command=stop_keylogger,

    state="disabled"
)

stop_button.grid(row=0, column=1, padx=10)

# ==========================================
# CLEAR LOGS BUTTON
# ==========================================

clear_button = tk.Button(

    root,

    text="CLEAR LOGS",

    width=25,

    height=2,

    bg="#333333",

    fg="white",

    font=("Arial", 10, "bold"),

    command=clear_logs
)

clear_button.pack(pady=10)

# ==========================================
# SHOW LOGS BUTTON
# ==========================================

show_button = tk.Button(

    root,

    text="SHOW LOGS",

    width=25,

    height=2,

    bg="#444444",

    fg="white",

    font=("Arial", 10, "bold"),

    command=show_logs
)

show_button.pack(pady=10)

# ==========================================
# EXIT BUTTON
# ==========================================

exit_button = tk.Button(

    root,

    text="EXIT",

    width=25,

    height=2,

    bg="#222222",

    fg="white",

    font=("Arial", 10, "bold"),

    command=exit_application
)

exit_button.pack(pady=10)

# ==========================================
# FOOTER
# ==========================================

footer_label = tk.Label(

    root,

    text="Educational Cybersecurity Project",

    font=("Arial", 9),

    bg="#121212",

    fg="gray"
)

footer_label.pack(side="bottom", pady=10)

# ==========================================
# RUN APPLICATION
# ==========================================

root.mainloop()
