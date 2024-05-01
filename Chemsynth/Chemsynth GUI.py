import random
import tkinter as GUI
from time import sleep
from threading import Thread
import os

class TankGame:
    def __init__(self):
        self.points = 100
        self.tanks = []
        self.tanks_required = []
        self.colors = ["red", "yellow", "green", "blue", "pink"]
        self.colors_iterated = ["red", "yellow", "green", "blue", "pink", "red"]
        self.game_number = 1
        self.game_running1 = False
        self.game_running2 = False
        self.current_tool = None
        self.total_points = 0

        self.root = GUI.Tk()
        self.root.title("Chemsynth")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.configure(background="purple")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.stirrer_image = GUI.PhotoImage(file=os.path.join(current_dir, "ToolSprites/Stirrer.png"))
        self.centrifuge_image = GUI.PhotoImage(file=os.path.join(current_dir, "ToolSprites/Centrifuge.png"))
        self.replicator_image = GUI.PhotoImage(file=os.path.join(current_dir, "ToolSprites/Replicator.png"))
        self.solvent_image = GUI.PhotoImage(file=os.path.join(current_dir, "ToolSprites/Solvent.png"))
        self.catalyst_image = GUI.PhotoImage(file=os.path.join(current_dir, "ToolSprites/Catalyst.png"))
        self.rainbow_image = GUI.PhotoImage(file=os.path.join(current_dir, "Rainbow.png"))

        self.start_button = GUI.Button(self.root, text="Play", command=self.tank_generator, font=("Helvetica", 25), background="cyan")
        self.start_button.place(x=300, y=225, width=200, height=50)

    def tank_generator(self):
        self.points = 100
        self.tanks = [random.choice(self.colors) for _ in range(10)]
        self.tanks_required = [random.choice(self.colors) for _ in range(10)]
        self.start_button.destroy()
        self.game_number += 1
        if self.game_number % 2 == 0:
            Rainbow_Thread1 = Thread(target=self.rainbow_movement1, args=(2,), daemon=True, name="Rainbow Movement 1")
            Rainbow_Thread1.start()
        else:
            Rainbow_Thread2 = Thread(target=self.rainbow_movement2, args=(2,), daemon=True, name="Rainbow Movement 2")
            Rainbow_Thread2.start()
        self.tank_screen()

    def select_tool(self, current=None):
        self.current_tool = current

    def use_tool(self, pos):
        if pos == self.rainbow1_pos or pos == self.rainbow2_pos:
            try:
                if self.current_tool == "stirrer":
                    self.stirrer(pos)
                elif self.current_tool == "centrifuge":
                    self.centrifuge(pos)
                elif self.current_tool == "replicator":
                    self.replicator(pos)
                elif self.current_tool == "solvent":
                    self.solvent(pos)
                elif self.current_tool == "catalyst":
                    self.catalyst(pos)
            except NameError:
                return

    def rainbow_movement1(self, interval_seconds):
        self.game_running1 = True
        n = 0
        possible_position = [1, 2, 3, 4, 5]
        self.rainbow1_pos = possible_position[n]
        self.rainbow2_pos = self.rainbow1_pos + 5
        rainbow1 = GUI.Label(self.root, image=self.rainbow_image, background="purple")
        rainbow1.place(x=n * 80, y=180, width=80, height=20)
        rainbow2 = GUI.Label(self.root, image=self.rainbow_image, background="purple")
        rainbow2.place(x=n * 80 + 400, y=180, width=80, height=20)

        while self.game_running1:
            sleep(interval_seconds)
            if self.game_running1:
                n = (n + 1) % 5
                self.rainbow1_pos = possible_position[n]
                self.rainbow2_pos = self.rainbow1_pos + 5
                rainbow1.place(x=n * 80, y=180, width=80, height=20)
                rainbow2.place(x=n * 80 + 400, y=180, width=80, height=20)

        if not self.game_running1:
            rainbow1.destroy()
            rainbow2.destroy()
            self.game_running1 = True

    def rainbow_movement2(self, interval_seconds):
        self.game_running2 = True
        n = 0
        possible_position = [1, 2, 3, 4, 5]
        self.rainbow1_pos = possible_position[n]
        self.rainbow2_pos = self.rainbow1_pos + 5
        rainbow1 = GUI.Label(self.root, image=self.rainbow_image, background="purple")
        rainbow1.place(x=n * 80, y=180, width=80, height=20)
        rainbow2 = GUI.Label(self.root, image=self.rainbow_image, background="purple")
        rainbow2.place(x=n * 80 + 400, y=180, width=80, height=20)

        while self.game_running2:
            sleep(interval_seconds)
            if self.game_running2:
                n = (n + 1) % 5
                self.rainbow1_pos = possible_position[n]
                self.rainbow2_pos = self.rainbow1_pos + 5
                rainbow1.place(x=n * 80, y=180, width=80, height=20)
                rainbow2.place(x=n * 80 + 400, y=180, width=80, height=20)

        if not self.game_running2:
            rainbow1.destroy()
            rainbow2.destroy()
            self.game_running2 = True

    def stirrer(self, pos):
        if pos == 1 or pos == 10:
            self.tank_screen()
        else:
            self.tanks[pos - 2], self.tanks[pos] = self.tanks[pos], self.tanks[pos - 2]
            self.points -= 2
            self.tank_screen()

    def centrifuge(self, pos):
        if pos == 1 or pos == 10:
            self.tank_screen()
        else:
            min_distance = min(pos - 1, 10 - pos)
            for i in range(min_distance, 0, -1):
                placeholder = self.tanks[pos - i - 1]
                self.tanks[pos - i - 1] = self.tanks[pos + i - 1]
                self.tanks[pos + i - 1] = placeholder
            self.points -= 2
            self.tank_screen()

    def replicator(self, pos):
        if pos == 10:
            self.tank_screen()
        else:
            for i in range(10, pos, -1):
                self.tanks[i - 1] = self.tanks[i - 2]
            self.points -= 2
            self.tank_screen()

    def solvent(self, pos):
        if pos == 10:
            self.tanks[pos - 1] = random.choice(self.colors)
            self.points -= 2
            self.tank_screen()
        else:
            for i in range(pos - 1, 9):
                self.tanks[i] = self.tanks[i + 1]
            self.tanks[9] = random.choice(self.colors)
            self.points -= 2
            self.tank_screen()

    def catalyst(self, pos):
        tanks_num = [self.colors.index(color) for color in self.tanks]
        tanks_same = [i for i, num in enumerate(tanks_num) if num == tanks_num[pos - 1]]
        tanks_affected = []
        color_selected = tanks_num[pos - 1]

        for i in tanks_same:
            if i <= pos - 1:
                interval = list(range(i, pos - 1))
            else:
                interval = list(range(i, pos - 1, -1))
            if set(tanks_same).issuperset(set(interval)):
                tanks_affected.append(i)
        
        for i in tanks_affected:
            self.tanks[i] = self.colors_iterated[color_selected + 1]
        
        self.points -= 2
        self.tank_screen()

    def tank_screen(self):
        if self.tanks == self.tanks_required:
            if self.game_number % 2 == 0:
                self.game_running1 = False
            else:
                self.game_running2 = False
            for widget in self.root.winfo_children():
                widget.destroy()
            self.total_points += self.points
            points_message = "Total Score: " + str(self.total_points)
            points_label = GUI.Label(self.root, text=points_message, font=("Helvetica", 25), background="purple")
            points_label.place(x=250, y=150, height=200, width=300)
            play_again_button = GUI.Button(self.root, text="Play Again", font=("Helvetica", 20), command=self.tank_generator, background="cyan")
            play_again_button.place(x=300, y=350, height=100, width=200)
        else:
            stirrer = GUI.Button(self.root, image=self.stirrer_image, command=lambda: self.select_tool("stirrer"), background="purple", borderwidth=0)
            stirrer.place(x=360, y=350, height=150, width=120)

            centrifuge = GUI.Button(self.root, image=self.centrifuge_image, command=lambda: self.select_tool("centrifuge"), background="purple", borderwidth=0)
            centrifuge.place(x=480, y=350, height=150, width=120)

            replicator = GUI.Button(self.root, image=self.replicator_image, command=lambda: self.select_tool("replicator"), background="purple", borderwidth=0)
            replicator.place(x=240, y=350, height=150, width=120)

            solvent = GUI.Button(self.root, image=self.solvent_image, command=lambda: self.select_tool("solvent"), background="purple", borderwidth=0)
            solvent.place(x=0, y=350, height=150, width=120)

            catalyst = GUI.Button(self.root, image=self.catalyst_image, command=lambda: self.select_tool("catalyst"), background="purple", borderwidth=0)
            catalyst.place(x=120, y=350, height=150, width=120)

            tank_buttons = []
            for i in range(10):
                tank_buttons.append(GUI.Button(self.root, command=lambda pos=i + 1: self.use_tool(pos), background=self.tanks[i]))
                tank_buttons[i].place(x=80 * i, y=200, height=80, width=80)

            req_labels = []
            for i in range(10):
                req_labels.append(GUI.Label(self.root, background=self.tanks_required[i]))
                req_labels[i].place(x=25 + 80 * i, y=280, height=20, width=30)

            points_message = "Score: " + str(self.points)
            points_label = GUI.Label(self.root, text=points_message, font=("Helvetica", 25), background="purple")
            points_label.place(x=250, y=0, height=150, width=300)

    def run(self):
        self.root.mainloop()

game = TankGame()
game.run()