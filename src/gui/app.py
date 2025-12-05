import tkinter as tk
from tkinter import ttk

from src.tamagotchi import Tamagotchi
from src.item import Item
from src.gui.components import CharacterDisplay, StatsPanel, ActionPanel, InventoryPanel, GamePanel   

class TamagotchiApp:
    STARTING_ITEMS = [
        ("Manzana", "comida", {"hambre": 20, "felicidad": 5}),
        ("Poción", "medicina", {"salud": 50}),
        ("Pelota", "juguete", {"felicidad": 15, "energia": -5}),
        ("Agua", "agua", {"sed": 10, "energia": 5}),
        ("Agua", "agua", {"sed": 10, "energia": 5})
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Tamagotchi")
        self.root.geometry("450x750")
        self.root.configure(bg="#f0f4f8")
        
        # Initialize Logic
        self.tama = Tamagotchi("Kakaroto", 0)
        self._add_starting_items()
        
        self.setup_ui()
        self.updateTicks()

    def _add_starting_items(self):
        """Agrega los objetos iniciales al inventario."""
        for nombre, tipo, efectos in self.STARTING_ITEMS:
            self.tama.inventario.add(Item(nombre, tipo, efectos))

    # -----------------------------
    # UI setup
    # -----------------------------
    def setup_ui(self):
        self._configure_notebook_style()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabs
        self.tab_general = tk.Frame(self.notebook, bg="#9C9C9C")
        self.tab_inventory = tk.Frame(self.notebook, bg="#9C9C9C")
        self.tab_game = tk.Frame(self.notebook, bg="#9C9C9C")

        self.notebook.add(self.tab_general, text="General")
        self.notebook.add(self.tab_inventory, text="Inventario")
        self.notebook.add(self.tab_game, text="Juego")
        
        self.setup_general_tab()
        self.setup_inventory_tab()
        self.setup_game_tab()

    def _configure_notebook_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#634848", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#634848",
            foreground="#ffffff",
            padding=[10, 5],
            font=("Helvetica", 10, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#634848")],
            foreground=[("selected", "#ffffff")]
        )

    # -----------------------------
    # Tabs
    # -----------------------------
    def setup_general_tab(self):
        self.char_display = CharacterDisplay(self.tab_general, self.tama)
        self.char_display.pack(fill="x")
        
        self.stats_panel = StatsPanel(self.tab_general, self.tama)
        self.stats_panel.pack(fill="x", padx=10, pady=10)
        
        self.action_panel = ActionPanel(self.tab_general, self.tama, self.on_action)
        self.action_panel.pack(fill="x", padx=10, pady=10)

    def setup_inventory_tab(self):
        self.inventory_panel = InventoryPanel(self.tab_inventory, self.tama, self.on_action)
        self.inventory_panel.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_game_tab(self):
        self.game_panel = GamePanel(self.tab_game, self.tama, self.on_action)
        self.game_panel.pack(fill="both", expand=True, padx=10, pady=10)

    # -----------------------------
    # Updates
    # -----------------------------
    def on_action(self):
        self.update_ui()

    def update_ui(self):
        self.char_display.update_display()
        self.stats_panel.update_stats()
        self.inventory_panel.refreshInventory()

    # -----------------------------
    # Timer loop
    # -----------------------------
    def updateTicks(self):
        if self.tama.vivo:
            self.tama.tick()
            self.update_ui()
            self.root.after(1000, self.updateTicks)
        else:
            self.update_ui()
            self.show_game_over()

    # -----------------------------
    # Game Over
    # -----------------------------
    def show_game_over(self):
        if hasattr(self, 'game_over_frame') and self.game_over_frame.winfo_exists():
            return

        self.game_over_frame = tk.Frame(self.root, bg="#2d3436")
        self.game_over_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        container = tk.Frame(self.game_over_frame, bg="#2d3436")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            container,
            text="GAME OVER",
            font=("Helvetica", 30, "bold"),
            fg="#ff7675",
            bg="#2d3436"
        ).pack(pady=20)
        
        tk.Button(
            container,
            text="Reiniciar",
            command=self.restart_game,
            font=("Helvetica", 14, "bold"),
            bg="#55efc4",
            fg="#2d3436"
        ).pack(pady=20)

    def restart_game(self):
        if hasattr(self, 'game_over_frame'):
            self.game_over_frame.destroy()
        
        if hasattr(self, 'notebook'):
            self.notebook.destroy()

        self.tama = Tamagotchi("Kakaroto", 0)
        self._add_starting_items()

        self.setup_ui()
        self.updateTicks()