import random
from tkinter import messagebox
from models import Developer
import tkinter as tk

class DeveloperManager:
    def __init__(self, game):
        self.game = game

    def create_new_developer_start(self):
        print("Creating new developer...")
        Developer.create_new_developer_start(self.game.developers)
        print("New developer created.")

    def open_hire_developer_selection(self):
        hire_window = tk.Toplevel(self.game.gui.root)
        hire_window.title("Hire Developer")

        def hire_beginner_developer():
            self.hire_developer("Beginner")
            hire_window.destroy()

        def hire_advanced_developer():
            self.hire_developer("Advanced")
            hire_window.destroy()

        def hire_professional_developer():
            self.hire_developer("Professional")
            hire_window.destroy()

        tk.Button(hire_window, text="Beginner Developer", command=hire_beginner_developer).pack(pady=10)
        tk.Button(hire_window, text="Advanced Developer", command=hire_advanced_developer).pack(pady=10)
        tk.Button(hire_window, text="Professional Developer", command=hire_professional_developer).pack(pady=10)

    def hire_developer(self, type):
        if type == "Beginner":
            new_developer = Developer.create_new_developer_beginner(self.game.developers)
        elif type == "Advanced":
            new_developer = Developer.create_new_developer_advanced(self.game.developers)
        elif type == "Professional":
            new_developer = Developer.create_new_developer_professional(self.game.developers)
        
        if new_developer:
            self.game.developers.append(new_developer)
            self.game.update_income_per_minute()
            self.game.gui.update_gui()
            print(f"{type} developer hired.")
        else:
            print(f"Failed to hire {type} developer.")

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
