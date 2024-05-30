import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import locale

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def reset_permissions_and_owner():
    folder_path = folder_path_entry.get()
    if folder_path:
        if not os.path.exists(folder_path):
            log_text.insert(tk.END, "Error: The specified folder does not exist.\n")
            log_text.see(tk.END)
            return

        log_text.insert(tk.END, f'Resetting permissions and owner for folder: "{folder_path}"\n')
        log_text.see(tk.END)

        def run_commands():
            try:
                # Set the code page to UTF-8
                chcp_command = ['chcp', '65001']
                subprocess.run(chcp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # Build the takeown command to reset ownership
                takeown_command = f'takeown /F "{folder_path}" /R /A /D Y'
                log_text.insert(tk.END, f"Running command: {takeown_command}\n")
                log_text.see(tk.END)
                # Execute the takeown command
                takeown_result = subprocess.run(takeown_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_text.insert(tk.END, f"takeown stdout: {takeown_result.stdout.decode(locale.getpreferredencoding(), errors='ignore')}\n")
                log_text.insert(tk.END, f"takeown stderr: {takeown_result.stderr.decode(locale.getpreferredencoding(), errors='ignore')}\n")
                log_text.see(tk.END)
                if takeown_result.returncode != 0:
                    raise Exception(takeown_result.stderr.decode(locale.getpreferredencoding(), errors='ignore'))

                # Build the icacls command to reset permissions
                icacls_command = f'icacls "{folder_path}" /reset /t /c'
                log_text.insert(tk.END, f"Running command: {icacls_command}\n")
                log_text.see(tk.END)
                # Execute the icacls command
                icacls_result = subprocess.run(icacls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_text.insert(tk.END, f"icacls stdout: {icacls_result.stdout.decode(locale.getpreferredencoding(), errors='ignore')}\n")
                log_text.insert(tk.END, f"icacls stderr: {icacls_result.stderr.decode(locale.getpreferredencoding(), errors='ignore')}\n")
                log_text.see(tk.END)
                if icacls_result.returncode != 0:
                    raise Exception(icacls_result.stderr.decode(locale.getpreferredencoding(), errors='ignore'))

                log_text.insert(tk.END, "Permissions and owner reset completed.\n")
            except Exception as e:
                log_text.insert(tk.END, f"Error: {e}\n")
            finally:
                log_text.see(tk.END)
                start_button.config(state=tk.NORMAL)

        # Disable the start button to prevent multiple simultaneous operations
        start_button.config(state=tk.DISABLED)
        # Run the commands in a separate thread
        threading.Thread(target=run_commands).start()
    else:
        log_text.insert(tk.END, "Please select a folder path.\n")
        log_text.see(tk.END)

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

if not is_admin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

# Create the main window
root = tk.Tk()
root.title("Reset Permissions and Owner")

# Create and place widgets
folder_path_label = tk.Label(root, text="Folder Path:")
folder_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

start_button = tk.Button(root, text="Start", command=reset_permissions_and_owner)
start_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

log_label = tk.Label(root, text="Log:")
log_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

log_text = ScrolledText(root, width=60, height=15)
log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
