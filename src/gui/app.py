from tkinter import Tk, Label, Button, StringVar
from tamagotchi import Tamagotchi

class TamagotchiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tamagotchi Game")
        
        self.tamagotchi = Tamagotchi("Kakaroto", 1)
        
        self.status_var = StringVar()
        self.update_status()

        self.status_label = Label(root, textvariable=self.status_var, font=("Arial", 14))
        self.status_label.pack(pady=20)

        self.feed_button = Button(root, text="Feed", command=self.feed)
        self.feed_button.pack(pady=5)

        self.water_button = Button(root, text="Water", command=self.water)
        self.water_button.pack(pady=5)

        self.play_button = Button(root, text="Play", command=self.play)
        self.play_button.pack(pady=5)

        self.sleep_button = Button(root, text="Sleep", command=self.sleep)
        self.sleep_button.pack(pady=5)

    def update_status(self):
        self.status_var.set(str(self.tamagotchi))

    def feed(self):
        self.tamagotchi.comer()
        self.update_status()

    def water(self):
        self.tamagotchi.beber()
        self.update_status()

    def play(self):
        self.tamagotchi.jugar()
        self.update_status()

    def sleep(self):
        self.tamagotchi.dormir()
        self.update_status()

def run_app():
    root = Tk()
    app = TamagotchiApp(root)
    root.mainloop()