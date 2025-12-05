import tkinter as tk

from src.gui.app import TamagotchiApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TamagotchiApp(root)
    root.mainloop()