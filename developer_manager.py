import random
from tkinter import messagebox
from models import Developer


class DeveloperManager:
    def __init__(self, game):
        self.game = game

    def create_new_developer(self):
        print("Creating new developer...")
        Developer.create_new_developer(self.game.developers)
        print("New developer created.")

    def train_developer(self):
        if self.game.developers:
            print("Training developer...")
            developer = random.choice(self.game.developers)
            skill_type = random.choice(["programming", "design", "marketing"])
            if self.game.balance >= self.game.training_cost:
                self.game.balance -= self.game.training_cost
                developer.train(skill_type)
                self.game.training_cost *= 1.2  # Increase the cost by 20%
                self.game.gui.update_gui()
                messagebox.showinfo(
                    "Training Completed", f"Developer trained in {skill_type}."
                )
                print(
                    f"Developer trained in {skill_type}. New training cost: ${self.game.training_cost:.2f}"
                )
            else:
                messagebox.showwarning(
                    "Insufficient Funds", "Not enough balance to train developer."
                )
                print("Not enough balance to train developer.")

    def specialize_developer(self):
        if self.game.developers:
            print("Specializing developer...")
            developer = random.choice(self.game.developers)
            specialization = random.choice(["Frontend", "Backend", "Fullstack"])
            developer.specialize(specialization)
            self.game.gui.update_gui()
            messagebox.showinfo(
                "Specialization", f"Developer specialized in {specialization}."
            )
            print(f"Developer specialized in {specialization}.")
