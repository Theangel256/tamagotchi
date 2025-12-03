from tkinter import Frame, Label, Button, StringVar, Tk

class TamagotchiGUI:
    def __init__(self, master, tamagotchi):
        self.master = master
        self.tamagotchi = tamagotchi
        self.master.title("Tamagotchi Game")
        
        self.status_var = StringVar()
        self.status_label = Label(master, textvariable=self.status_var)
        self.status_label.pack()

        self.feed_button = Button(master, text="Feed", command=self.feed)
        self.feed_button.pack()

        self.water_button = Button(master, text="Water", command=self.water)
        self.water_button.pack()

        self.play_button = Button(master, text="Play", command=self.play)
        self.play_button.pack()

        self.sleep_button = Button(master, text="Sleep", command=self.sleep)
        self.sleep_button.pack()

        self.update_status()

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

    def update_status(self):
        self.status_var.set(str(self.tamagotchi))