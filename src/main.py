import os
import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import locale
import gettext
from tkinter import ttk

# 获取系统语言
def get_system_language():
    locale.setlocale(locale.LC_ALL, '')
    return locale.getlocale()[0]

# 设置语言环境
def set_language(language_code):
    locale_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locales')
    lang = gettext.translation('messages', localedir=locale_dir, languages=[language_code], fallback=True)
    lang.install()
    global _
    _ = lang.gettext

# 获取系统语言并设置语言环境
system_language = get_system_language()
if system_language in ['zh_CN', 'zh_TW', 'en']:
    set_language(system_language)
else:
    set_language('en')  # 默认为英文

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def reset_permissions_and_owner():
    folder_path = folder_path_entry.get()
    if folder_path:
        if not os.path.exists(folder_path):
            log_text.insert(tk.END, _("Error: The specified folder does not exist.\n"))
            log_text.see(tk.END)
            return

        # 将正斜杠替换为反斜杠
        folder_path = folder_path.replace('/', '\\')
        
        log_text.insert(tk.END, _('Resetting permissions and ownership for folder "{}".\n').format(folder_path))
        log_text.see(tk.END)

        def run_commands():
            try:
                # 设置代码页为UTF-8
                chcp_command = ['chcp', '65001']
                subprocess.run(chcp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                # 构建icacls命令以重置权限
                icacls_command = f'icacls "{folder_path}" /reset /t /c'
                log_text.insert(tk.END, _("Running command: {}\n").format(icacls_command))
                log_text.see(tk.END)
                # 执行icacls命令
                icacls_result = subprocess.run(icacls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_text.insert(tk.END, f"icacls stdout: {icacls_result.stdout.decode('gbk', errors='ignore')}\n")
                log_text.insert(tk.END, f"icacls stderr: {icacls_result.stderr.decode('gbk', errors='ignore')}\n")
                log_text.see(tk.END)
                if icacls_result.returncode != 0:
                    raise Exception(icacls_result.stderr.decode('gbk', errors='ignore'))

                # 在运行takeown之前检查文件夹是否仍然存在
                if not os.path.exists(folder_path):
                    raise Exception(_("The specified folder does not exist after running icacls."))

                # 构建takeown命令以重置所有权
                takeown_command = f'takeown /F "{folder_path}" /R /A /D Y'
                log_text.insert(tk.END, _("Running command: {}\n").format(takeown_command))
                log_text.see(tk.END)
                # 执行takeown命令
                takeown_result = subprocess.run(takeown_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                log_text.insert(tk.END, f"takeown stdout: {takeown_result.stdout.decode('utf-8', errors='ignore')}\n")
                log_text.insert(tk.END, f"takeown stderr: {takeown_result.stderr.decode('utf-8', errors='ignore')}\n")
                log_text.see(tk.END)
                if takeown_result.returncode != 0:
                    raise Exception(takeown_result.stderr.decode('utf-8', errors='ignore'))

                log_text.insert(tk.END, _("Permissions and ownership reset complete.\n"))
            except Exception as e:
                log_text.insert(tk.END, _("Error: {}\n").format(e))
            finally:
                log_text.see(tk.END)
                start_button.config(state=tk.NORMAL)

        # 禁用开始按钮以防止同时进行多个操作
        start_button.config(state=tk.DISABLED)
        # 在单独的线程中运行命令
        threading.Thread(target=run_commands).start()
    else:
        log_text.insert(tk.END, _("Please select a folder path.\n"))
        log_text.see(tk.END)

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_path_entry.delete(0, tk.END)
    folder_path_entry.insert(0, folder_path)

def change_language():
    selected_language = language_combobox.get()
    set_language(selected_language)
    refresh_gui_text()

def refresh_gui_text():
    root.title(_("Reset Permissions and Ownership"))
    folder_path_label.config(text=_("Folder Path:"))
    browse_button.config(text=_("Browse"))
    start_button.config(text=_("Start"))
    log_label.config(text=_("Log:"))
    language_label.config(text=_("Language:"))

if not is_admin():
    # 以管理员权限重新运行程序，并传递系统语言作为参数
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}" "{system_language}"', None, 1)
    sys.exit()
else:
    # 如果脚本以管理员身份运行，从命令行参数中获取语言并设置语言环境
    if len(sys.argv) > 1:
        system_language = sys.argv[1]
        set_language(system_language)

# 设置DPI感知
try:
    # Windows 10 Version 1607 and later
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception as e:
    try:
        # Windows 8.1 and later
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e:
        print(f"Error setting DPI awareness: {e}")

# 创建主窗口
root = tk.Tk()
root.title(_("Reset Permissions and Ownership"))

# 创建并放置控件
folder_path_label = tk.Label(root, text=_("Folder Path:"))
folder_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

browse_button = tk.Button(root, text=_("Browse"), command=browse_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

start_button = tk.Button(root, text=_("Start"), command=reset_permissions_and_owner)
start_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

log_label = tk.Label(root, text=_("Log:"))
log_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

log_text = ScrolledText(root, width=60, height=15)
log_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

language_label = tk.Label(root, text=_("Language:"))
language_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")

language_combobox = ttk.Combobox(root, values=['en', 'zh_CN', 'zh_TW'], state='readonly')
language_combobox.grid(row=4, column=1, padx=5, pady=5, sticky="w")
language_combobox.set(system_language)
language_combobox.bind("<<ComboboxSelected>>", lambda event: change_language())

# 初始化GUI文本
refresh_gui_text()

# 运行主循环
root.mainloop()