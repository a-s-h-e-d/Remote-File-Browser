import subprocess
import tkinter as tk
from tkinter import messagebox

hwid = str(str(subprocess.check_output('wmic csproduct get uuid')).strip().replace(r"\r", "").split(r"\n")[1].strip())
root = tk.Tk()
root.withdraw()

messagebox.showinfo("Xenon", hwid)
root.destroy()