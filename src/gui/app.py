import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from src.tamagotchi import Tamagotchi
from src.item import Item
from src.game import Game
from src.gui.components import CharacterDisplay, StatsPanel, ActionPanel, InventoryPanel, StatusIndicators, LogPanel


class TamagotchiApp:
    STARTING_ITEMS = [
        ("Manzana", "comida", {"hambre": 20, "felicidad": 5}),
        ("Poción", "medicina", {"salud": 50}),
        ("Pelota", "juguete", {"felicidad": 15, "energia": -5}),
        ("Agua", "agua", {"sed": 15, "energia": 5}),
        ("Agua", "agua", {"sed": 15, "energia": 5}),
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tamagotchi")
        self.root.geometry("540x860")
        self.root.configure(bg="#f0f4f8")
        
        # Centrar la ventana en el monitor
        self.root.update_idletasks()
        window_width = 540
        window_height = 860
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Pedir nombre
        nombre = simpledialog.askstring("Nombre", "¿Cómo quieres llamar a tu Tamagotchi?", parent=self.root)
        if not nombre:
            nombre = "Kakaroto"

        # Modelo y controlador
        self.tama = Tamagotchi(nombre, 0)
        self.game = Game(self.tama)
        self._add_starting_items()

        # UI
        self._setup_menu()
        self._setup_notebook()
        self.update_ui()

        # Loop del juego (tick)
        self.root.after(1000, self.update_loop)

    def _add_starting_items(self):
        for nombre, tipo, efectos in self.STARTING_ITEMS:
            self.tama.inventario.add(Item(nombre, tipo, efectos))

    def _setup_menu(self):
        menubar = tk.Menu(self.root)
        ayuda = tk.Menu(menubar, tearoff=0)
        ayuda.add_command(label="Reglas del juego", command=self._mostrar_ayuda)
        ayuda.add_command(label="Mostrar estado detallado", command=self._show_status_popup)
        ayudat = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda)
        self.root.config(menu=menubar)

    def _setup_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side="top", fill="both", expand=True, padx=8, pady=8)

        self.tab_general = tk.Frame(self.notebook, bg="#f7f7f7")
        self.tab_inventario = tk.Frame(self.notebook, bg="#f7f7f7")

        self.notebook.add(self.tab_general, text="General")
        self.notebook.add(self.tab_inventario, text="Inventario")

        # Panels
        self.char_display = CharacterDisplay(self.tab_general, self.tama)
        self.char_display.pack(fill="x", pady=(6, 0))
        
        self.status_indicators = StatusIndicators(self.tab_general, self.tama)
        self.status_indicators.pack(fill="x", padx=8, pady=4)

        self.stats_panel = StatsPanel(self.tab_general, self.tama)
        self.stats_panel.pack(fill="x", padx=8, pady=8)
        
        self.action_panel = ActionPanel(self.tab_general, self.tama, self.game, self._on_event)
        self.action_panel.pack(fill="x", padx=8, pady=6)
        
        # LogPanel ahora dentro de General
        self.log_panel = LogPanel(self.tab_general)
        self.log_panel.pack(fill="both", expand=True, padx=8, pady=8)

        self.inventory_panel = InventoryPanel(self.tab_inventario, self.tama, self.game, self._on_event)
        self.inventory_panel.pack(fill="both", expand=True, padx=8, pady=8)

    def _on_event(self, mensaje: str):
        # Callback desde componentes; muestra mensaje y actualiza UI
        if mensaje:
            self.log_panel.add_message(mensaje)
        self.update_ui()

    def update_ui(self):
        self.char_display.update_display()
        self.status_indicators.update_status()
        self.stats_panel.update_stats()
        self.inventory_panel.refreshInventory()

    def update_loop(self):
        # Avanza el juego por tick automático (si está vivo)
        if self.tama.vivo:
            msg = self.game.avanzar_turno()
            if msg:
                self.log_panel.add_message(msg)
            self.update_ui()
            self.root.after(1000, self.update_loop)
        else:
            # Mostrar overlay Game Over
            self._show_game_over()

    # -----------
    # Utilidades
    # -----------
    def _mostrar_ayuda(self):
        texto = (
            "Reglas básicas:\n"
            "- Mantén hambre, sed y salud lejos de 0.\n"
            "- Si 3 atributos están críticos durante varios turnos, puede morir.\n"
            "- Eventos aleatorios pueden afectar su estado.\n"
            "- Usa items desde Inventario. Hay capacidad máxima.\n"
            "- Puedes saltar turno con el botón correspondiente.\n"
            "\nObjetivo: Mantener a la mascota viva el mayor tiempo posible."
        )
        messagebox.showinfo("Reglas del juego", texto)

    def _show_status_popup(self):
        messagebox.showinfo("Estado detallado", self.tama.mostrar_estado_detallado())

    def _show_game_over(self):
        # Overlay simple
        overlay = tk.Frame(self.root, bg="#2d3436")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        c = tk.Frame(overlay, bg="#2d3436")
        c.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(c, text="GAME OVER", font=("Helvetica", 30, "bold"), fg="#ff7675", bg="#2d3436").pack(pady=10)
        tk.Button(c, text="Reiniciar", command=self._restart, bg="#55efc4").pack(pady=8)
        tk.Button(c, text="Estado detallado", command=self._show_status_popup, bg="#dfe6e9").pack(pady=8)

    def _restart(self):
        # Reiniciar la app (recrea modelo y controlador)
        for widget in self.root.winfo_children():
            widget.destroy()
        # recrear todo
        self.__init__(self.root)