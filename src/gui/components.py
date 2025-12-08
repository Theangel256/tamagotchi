import tkinter as tk
from tkinter import font, messagebox

GREEN = "#55efc4"
GREEN_DARK = "#00b894"
RED = "#ff7675"
RED_DARK = "#d63031"
YELLOW = "#ffeaa7"
PURPLE = "#a29bfe"
GREY = "#dfe6e9"
TEXT_COLOR = "#2d3436"


class CharacterDisplay(tk.Frame):
    def __init__(self, parent, tamagotchi, bg_color="#f0f4f8"):
        super().__init__(parent, bg=bg_color)
        self.tamagotchi = tamagotchi
        self.bg_color = bg_color
        self.heading_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.sub_font = font.Font(family="Helvetica", size=10)

        self.name_label = tk.Label(self, text=self.tamagotchi.nombre, font=self.heading_font, bg=self.bg_color, fg="#ff6b6b")
        self.name_label.pack(pady=(12, 2))

        # Info Frame (Vivo, Evolucion, Edad)
        self.info_frame = tk.Frame(self, bg=self.bg_color)
        self.info_frame.pack(pady=4)

        self.status_label = tk.Label(self.info_frame, text="VIVO", font=("Helvetica", 10, "bold"), bg=GREEN, fg=GREEN_DARK, padx=8, pady=2)
        self.status_label.pack(side="left", padx=4)

        self.evo_label = tk.Label(self.info_frame, text="", font=self.sub_font, bg=self.bg_color, fg=TEXT_COLOR)
        self.evo_label.pack(side="left", padx=4)

        self.age_label = tk.Label(self.info_frame, text="", font=self.sub_font, bg=self.bg_color, fg=TEXT_COLOR)
        self.age_label.pack(side="left", padx=4)

        self.char_label = tk.Label(self, text="(◕‿◕)", font=("Helvetica", 56), bg=self.bg_color, fg=TEXT_COLOR)
        self.char_label.pack(pady=12)

    def update_display(self):
        # Actualizar textos
        self.evo_label.config(text=f"{self.tamagotchi.evolucion}")
        self.age_label.config(text=f"Edad: {self.tamagotchi.edad}")

        if not self.tamagotchi.vivo:
            self.status_label.config(text="MUERTO", bg=RED, fg=RED_DARK)
            self.char_label.config(text="(x_x)")
        else:
            self.status_label.config(text="VIVO", bg=GREEN, fg=GREEN_DARK)
            # Cara dinámica
            emocion = self.tamagotchi.estado_emocional
            cara = "(◕‿◕)" # Default / Eufórico
            if emocion == "Contento": cara = "(•‿•)"
            elif emocion == "Cansado": cara = "(-_-)"
            elif emocion == "Deprimido": cara = "(T_T)"
            
            self.char_label.config(text=cara)


class StatsPanel(tk.Frame):
    STATS_MAP = {
        "hambre": "Hambre",
        "sed": "Sed",
        "felicidad": "Felicidad",
        "energia": "Energía",
        "salud": "Salud",
        "limpieza": "Limpieza"
    }

    def __init__(self, parent, tamagotchi, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, padx=12, pady=12)
        self.tamagotchi = tamagotchi
        self.bg_color = bg_color
        self.label_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.bars = {}
        for key, label in self.STATS_MAP.items():
            self._create_row(key, label)

    def _create_row(self, key, label):
        frame = tk.Frame(self, bg=self.bg_color)
        frame.pack(fill="x", pady=3)

        label_frame = tk.Frame(frame, bg=self.bg_color)
        label_frame.pack(fill="x")
        tk.Label(label_frame, text=label, font=self.label_font, bg=self.bg_color, fg=TEXT_COLOR).pack(side="left")
        val_label = tk.Label(label_frame, text="100%", font=self.label_font, bg=self.bg_color, fg=TEXT_COLOR)
        val_label.pack(side="right")

        canvas = tk.Canvas(frame, height=12, bg=GREY, highlightthickness=0)
        canvas.pack(fill="x", pady=(3, 0))
        bar = canvas.create_rectangle(0, 0, 0, 12, fill=GREEN, width=0)

        self.bars[key] = {"canvas": canvas, "bar": bar, "val_label": val_label}

    def update_stats(self):
        values = {
            "hambre": self.tamagotchi.hambre,
            "sed": self.tamagotchi.sed,
            "felicidad": self.tamagotchi.felicidad,
            "energia": self.tamagotchi.energia,
            "salud": self.tamagotchi.salud,
            "limpieza": self.tamagotchi.limpieza
        }
        for k, v in values.items():
            self._update_bar(k, v)

    def _update_bar(self, key, value):
        info = self.bars[key]
        canvas = info["canvas"]
        bar = info["bar"]
        label = info["val_label"]
        label.config(text=f"{value}%")
        canvas.update_idletasks()
        width = max(canvas.winfo_width(), 220)
        size = (value / 100) * width
        color = GREEN if value > 60 else (YELLOW if value > 30 else RED)
        canvas.coords(bar, 0, 0, size, 12)
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

    def __init__(self, parent, tamagotchi, controlador, callback_ui, bg_color="#f0f4f8"):
        super().__init__(parent, bg=bg_color)
        self.tamagotchi = tamagotchi
        self.controlador = controlador  # Game controller
        self.callback_ui = callback_ui

        for i, (texto, metodo, color) in enumerate(self.ACTIONS):
            # Usar controlador en lugar de tamagotchi para acciones con eventos
            func = getattr(self.controlador, metodo)
            btn = tk.Button(self, text=texto, command=lambda f=func: self._do_action(f), bg=color, relief="flat", font=("Helvetica", 9, "bold"))
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="ew")
            self.grid_columnconfigure(i % 3, weight=1)

        # Saltar turno
        self.skip_btn = tk.Button(self, text="⏭️ Saltar turno", command=self._skip_turn, bg="#ffd79b", relief="raised")
        self.skip_btn.grid(row=2, column=0, columnspan=3, sticky="ew", padx=6, pady=(8, 0))

    def _do_action(self, f):
        f()
        # después de una acción, avanzar turno (coste temporal)
        if self.controlador:
            msg = self.controlador.avanzar_turno()
        else:
            msg = "Acción realizada"
        if self.callback_ui:
            self.callback_ui(msg)

    def _skip_turn(self):
        if self.controlador:
            msg = self.controlador.saltar_turno()
            if self.callback_ui:
                self.callback_ui(msg)


class InventoryPanel(tk.Frame):
    def __init__(self, parent, tamagotchi, controlador, callback_ui, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, padx=12, pady=12)
        self.tamagotchi = tamagotchi
        self.controlador = controlador
        self.callback_ui = callback_ui
        self.bg_color = bg_color

        tk.Label(self, text="Inventario", font=("Helvetica", 14, "bold"), bg=bg_color).pack(pady=(0, 8))
        self.items_frame = tk.Frame(self, bg=bg_color)
        self.items_frame.pack(fill="both", expand=True)
        self.refreshInventory()

    def refreshInventory(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        items = self.tamagotchi.inventario.items
        if not items:
            tk.Label(self.items_frame, text="Inventario vacío", bg=self.bg_color, fg="#636e72").pack(pady=12)
            return
        for nombre, lista in items.items():
            cantidad = len(lista)
            item_ref = lista[0]
            row = tk.Frame(self.items_frame, bg=GREY, padx=6, pady=6)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=f"{nombre} (x{cantidad})\n{item_ref.tipo}", bg=GREY, justify="left").pack(side="left")
            tk.Button(row, text="Usar", command=lambda n=nombre: self._usar(n), bg=GREEN, relief="flat").pack(side="right")

    def _usar(self, nombre):
        resultado = self.tamagotchi.usar_item(nombre)
        if self.callback_ui:
            self.callback_ui(resultado)
        self.refreshInventory()

class StatusIndicators(tk.Frame):
    def __init__(self, parent, tamagotchi, bg_color="#ffffff"):
        super().__init__(parent, bg=bg_color, pady=8)
        self.tamagotchi = tamagotchi
        self.bg_color = bg_color
        
        # Container for 3 boxes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.lbl_general = self._create_box(0, "General")
        self.lbl_emocional = self._create_box(1, "Emocional")
        self.lbl_riesgo = self._create_box(2, "Riesgo")

    def _create_box(self, col, title):
        frame = tk.Frame(self, bg=self.bg_color, padx=4)
        frame.grid(row=0, column=col, sticky="ew")
        
        tk.Label(frame, text=title, font=("Helvetica", 8), bg=self.bg_color, fg="#636e72").pack()
        lbl = tk.Label(frame, text="--", font=("Helvetica", 9, "bold"), width=10, pady=4)
        lbl.pack(fill="x")
        return lbl

    def update_status(self):
        # General
        gen = self.tamagotchi.estado_general
        color_gen = GREEN if gen in ["Excelente", "Bueno"] else (YELLOW if gen == "Regular" else RED)
        self.lbl_general.config(text=gen, bg=color_gen, fg=TEXT_COLOR)

        # Emocional
        emo = self.tamagotchi.estado_emocional
        color_emo = GREEN if emo in ["Eufórico", "Contento"] else (YELLOW if emo == "Cansado" else RED)
        self.lbl_emocional.config(text=emo, bg=color_emo, fg=TEXT_COLOR)

        # Riesgo
        risk = self.tamagotchi.riesgo_de_muerte
        color_risk = GREEN if risk == "Bajo" else (YELLOW if risk == "Medio" else RED)
        self.lbl_riesgo.config(text=risk, bg=color_risk, fg=TEXT_COLOR)


class LogPanel(tk.Frame):
    def __init__(self, parent, bg_color="#ededed"):
        super().__init__(parent, bg=bg_color, height=100)
        self.pack_propagate(False) # Respetar altura
        
        tk.Label(parent, text="Registro de Eventos", bg=bg_color, font=("Helvetica", 8, "bold"), anchor="w").pack(fill="x", padx=8, pady=(4,0))

        self.text_area = tk.Text(self, bg="#dfe6e9", fg=TEXT_COLOR, font=("Consolas", 9), state="disabled", padx=4, pady=4)
        self.scrollbar = tk.Scrollbar(self, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.pack(side="left", fill="both", expand=True)

    def add_message(self, message: str):
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")