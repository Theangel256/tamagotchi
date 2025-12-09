import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk

from src.gui.app import TamagotchiApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TamagotchiApp(root)
    root.mainloop()