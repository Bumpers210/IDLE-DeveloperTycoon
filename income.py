import threading
from models import Developer
import tkinter as tk


class Income:
    def __init__(self, game):
        self.game = game
        
    def start_income_timer(self):
        self.income_timer = threading.Timer(1, self.generate_income)
        self.income_timer.daemon = True
        self.income_timer.start()

    def generate_income(self):
        total_salary = sum(dev.salary for dev in self.game.developers)
        income_per_second = (
            self.income_per_minute / 60
        )  
        salary_per_second = total_salary / (
            60 * 60
        )  
        self.game.balance += income_per_second
        self.game.gui.update_gui()
        self.income_timer = threading.Timer(1, self.generate_income)
        self.income_timer.daemon = True
        self.income_timer.start()

    def update_income_per_minute(self):
        total_salary = sum(dev.salary for dev in self.game.developers)
        project_income = (
            sum(project.programming for project in self.game.completed_projects_list)
            + sum(project.design for project in self.game.completed_projects_list)
            + sum(project.marketing for project in self.game.completed_projects_list)
            / 3  # Balanced Income/Minute
        )
        self.income_per_minute = project_income - (total_salary / 60)
