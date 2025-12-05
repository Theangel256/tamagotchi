import tkinter as tk
from tkinter import ttk, font
import random


# ===========================
#  COLORS & CONSTANTS
# ===========================
GREEN = "#55efc4"
GREEN_DARK = "#00b894"
RED = "#ff7675"
RED_DARK = "#d63031"
YELLOW = "#ffeaa7"
BLUE = "#74b9ff"
PURPLE = "#a29bfe"
GREY = "#dfe6e9"
TEXT_COLOR = "#2d3436"


class CharacterDisplay(tk.Frame):
    def __init__(self, parent, tamagotchi, bg_color="#f0f4f8"):
        super().__init__(parent, bg=bg_color)
        self.tamagotchi = tamagotchi
        self.bg_color = bg_color
        
        self.heading_font = font.Font(family="Helvetica", size=24, weight="bold")
        
        # Header
        self.name_label = tk.Label(
            self,
            text=self.tamagotchi.nombre,
            font=self.heading_font,
            bg=self.bg_color,
            fg="#ff6b6b"
        )
        self.name_label.pack(pady=(20, 5))
        
        # Status label
        self.status_label = tk.Label(
            self,
            text="VIVO",
            font=("Helvetica", 10, "bold"),
            bg=GREEN,
            fg=GREEN_DARK,
            padx=10,
            pady=2
        )
        self.status_label.pack(pady=5)

        # Character face
        self.char_label = tk.Label(
            self,
            text="(◕‿◕)",
            font=("Helvetica", 60),
            bg=self.bg_color,
            fg=TEXT_COLOR
        )
        self.char_label.pack(pady=20)

    def update_display(self):
        """Actualiza el estado visual del personaje."""
        if not self.tamagotchi.vivo:
            self.status_label.config(text="MUERTO", bg=RED, fg=RED_DARK)
            self.char_label.config(text="(x_x)")
        else:
            self.status_label.config(text="VIVO", bg=GREEN, fg=GREEN_DARK)
            self.char_label.config(text="(◕‿◕)")


class StatsPanel(tk.Frame):
    STATS_MAP = {
        "hambre": "Hambre",
        "sed": "Sed",
        "felicidad": "Felicidad",
        "energia": "Energia",
        "salud": "Salud",
        "limpieza": "Limpieza"
    }

    def __init__(self, parent, tamagotchi, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, padx=20, pady=20)
        self.tamagotchi = tamagotchi
        self.bg_color = bg_color
        self.label_font = font.Font(family="Helvetica", size=10, weight="bold")

        self.bars = {}
        for key, label in self.STATS_MAP.items():
            self._create_stat_row(key, label)

    def _create_stat_row(self, key, label):
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="x", pady=5)

        # Label + numeric value
        label_frame = tk.Frame(frame, bg=self.bg_color)
        label_frame.pack(fill="x")

        tk.Label(label_frame, text=label, font=self.label_font, bg=self.bg_color, fg=TEXT_COLOR)\
            .pack(side="left")

        val_label = tk.Label(label_frame, text="100%", font=self.label_font, bg=self.bg_color, fg=TEXT_COLOR)
        val_label.pack(side="right")

        # Progress bar
        canvas = tk.Canvas(frame, height=15, bg=GREY, highlightthickness=0)
        canvas.pack(fill="x", pady=(2, 0))
        bar = canvas.create_rectangle(0, 0, 0, 15, fill=GREEN, width=0)

        self.bars[key] = {
            "canvas": canvas,
            "bar": bar,
            "val_label": val_label
        }

    def update_stats(self):
        """Actualiza todas las barras de atributos."""
        stat_values = {
            "hambre": self.tamagotchi.hambre,
            "sed": self.tamagotchi.sed,
            "felicidad": self.tamagotchi.felicidad,
            "energia": self.tamagotchi.energia,
            "salud": self.tamagotchi.salud,
            "limpieza": self.tamagotchi.limpieza
        }

        for stat, value in stat_values.items():
            self._update_single_bar(stat, value)

    def _update_single_bar(self, stat_name, value):
        info = self.bars[stat_name]
        canvas = info["canvas"]
        bar = info["bar"]
        label = info["val_label"]

        label.config(text=f"{value}%")
        canvas.update_idletasks()

        canvas_width = max(canvas.winfo_width(), 200)
        width = (value / 100) * canvas_width

        # Color by value
        if value <= 30:
            color = RED
        elif value <= 60:
            color = YELLOW
        else:
            color = GREEN

        canvas.coords(bar, 0, 0, width, 15)
        canvas.itemconfig(bar, fill=color)


class ActionPanel(tk.Frame):
    ACTIONS = [
        ("🍔 Comer", "comer", "#ffeaa7"),
        ("💧 Beber", "beber", "#74b9ff"),
        ("🎾 Jugar", "jugar", "#a29bfe"),
        ("💤 Dormir", "dormir", "#dfe6e9"),
        ("✨ Limpiar", "banarse", "#81ecec"),
        ("💊 Curar", "curar", "#ff7675")
    ]

    def __init__(self, parent, tamagotchi, on_action_callback, bg_color="#f0f4f8"):
        super().__init__(parent, bg=bg_color)
        self.tamagotchi = tamagotchi
        self.callback = on_action_callback

        for i, (text, method, color) in enumerate(self.ACTIONS):
            func = getattr(self.tamagotchi, method)
            btn = tk.Button(
                self,
                text=text,
                command=lambda f=func: self.perform_action(f),
                bg=color, relief="flat",
                font=("Helvetica", 9, "bold"),
                activebackground=color
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="ew")
            self.grid_columnconfigure(i % 3, weight=1)

    def perform_action(self, command):
        command()
        if self.callback:
            self.callback()


class InventoryPanel(tk.Frame):
    def __init__(self, parent, tamagotchi, on_action_callback, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, padx=20, pady=20)
        self.tamagotchi = tamagotchi
        self.callback = on_action_callback
        self.bg_color = bg_color
        
        tk.Label(self, text="Inventario", font=("Helvetica", 14, "bold"), bg=bg_color)\
            .pack(pady=(0, 10))
        
        self.items_frame = tk.Frame(self, bg=bg_color)
        self.items_frame.pack(fill="both", expand=True)
        
        self.refreshInventory()

    def refreshInventory(self):
        """Redibuja el inventario."""
        for widget in self.items_frame.winfo_children():
            widget.destroy()
            
        items = self.tamagotchi.inventario.items
        
        if not items:
            tk.Label(self.items_frame, text="Inventario vacío", bg=self.bg_color, fg="#636e72")\
                .pack(pady=20)
            return

        for nombre, lista in items.items():
            count = len(lista)
            item_ref = lista[0]
            item_frame = tk.Frame(self.items_frame, bg=GREY, padx=10, pady=5)
            item_frame.pack(fill="x", pady=2)
            
            tk.Label(item_frame, text=f"{nombre} (x{count})\n{item_ref.tipo}", bg=GREY, justify="left")\
                .pack(side="left")
            
            tk.Button(
                item_frame,
                text="Usar",
                command=lambda n=nombre: self.use_item(n),
                bg=GREEN, relief="flat"
            ).pack(side="right")

    def use_item(self, nombre):
        self.tamagotchi.usar_item(nombre)
        self.refreshInventory()
        if self.callback:
            self.callback()


class GamePanel(tk.Frame):
    """Minijuego simple: Adivinar número."""
    def __init__(self, parent, tamagotchi, on_action_callback, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, padx=20, pady=20)
        self.tamagotchi = tamagotchi
        self.callback = on_action_callback

        tk.Label(self, text="Minijuego: Adivina el Número",
                 font=("Helvetica", 14, "bold"), bg=bg_color).pack(pady=(0, 10))

        self.secret_number = random.randint(1, 10)
        self.attempts = 0

        tk.Label(self, text="Adivina un número entre 1 y 10:", bg=bg_color).pack(pady=5)
        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack(pady=5)

        tk.Button(self, text="Adivinar", command=self._check_guess,
                  bg=PURPLE, relief="flat").pack(pady=5)

        self.result_label = tk.Label(self, text="", bg=bg_color, fg="blue")
        self.result_label.pack(pady=5)

    def _check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.result_label.config(text="Introduce un número válido.")
            self.guess_entry.delete(0, tk.END)
            return

        self.attempts += 1

        if guess == self.secret_number:
            self.result_label.config(text=f"¡Correcto! Intentos: {self.attempts}")
            self._reward_tamagotchi()
            self._reset_game()
        elif guess < self.secret_number:
            self.result_label.config(text="Demasiado bajo.")
        else:
            self.result_label.config(text="Demasiado alto.")

        self.guess_entry.delete(0, tk.END)

    def _reward_tamagotchi(self):
        # Recompensa básica y segura
        self.tamagotchi._Tamagotchi__felicidad = min(100, self.tamagotchi.felicidad + 10)
        if self.callback:
            self.callback()

    def _reset_game(self):
        self.secret_number = random.randint(1, 10)
        self.attempts = 0
