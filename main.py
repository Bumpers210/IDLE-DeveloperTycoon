import json
import time
import random
import threading
import tkinter as tk
from tkinter import messagebox
from gui import GameGUI
from project_selector import ProjectSelector
from game_storage import GameStorage
from models import Project, Developer, Research
from project_manager import ProjectManager
from event_manager import EventManager
from research_manager import ResearchManager
from developer_manager import DeveloperManager


class Game:
    AUTO_SAVE_INTERVAL = 60  # seconds
    INITIAL_TRAINING_COST = 10

    def __init__(self):
        print("Initializing Game...")
        self.storage = GameStorage("game_data.db")
        self.income_per_minute = 0  # Ensure initial income is 0
        self.developers = Developer.load_developers_from_db(self.storage)
        self.projects = self.load_projects()
        self.researches = self.load_researches()
        self.current_project = None
        self.current_research = None
        self.balance = 0.0
        self.completed_projects = 0
        self.completed_projects_list = []
        self.project_in_progress = False
        self.remaining_project_time = 0
        self.training_cost = self.INITIAL_TRAINING_COST
        self.remaining_research_time = 0
        self.auto_save_thread = threading.Thread(
            target=self.auto_save_game, daemon=True
        )
        self.auto_save_thread.start()

        self.event_manager = EventManager(self)  # Initialize EventManager
        self.gui = GameGUI(self)
        self.project_selector = ProjectSelector(self)
        self.project_manager = ProjectManager(self)
        self.research_manager = ResearchManager(self)
        self.developer_manager = DeveloperManager(self)

        GameStorage.create_tables_if_not_exist()
        self.storage.load_game(self)

        if not self.developers:
            self.developer_manager.create_new_developer()

        self.update_income_per_minute()  # Update income per minute after loading game data

        if self.current_project and self.remaining_project_time > 0:
            self.gui.update_project_timer(
                self.current_project.name,
                self.remaining_project_time,
                self.current_project.duration,
            )
            self.gui.enable_resume_button()

        self.start_income_timer()
        self.gui.update_gui()  # Ensure the GUI is updated with the correct initial values

        self.random_events_thread = threading.Thread(
            target=self.event_manager.start_random_events, daemon=True
        )
        self.random_events_thread.start()

        print("Game Initialized.")

    def load_projects(self):
        print("Loading projects from database...")
        project_data = self.storage.get_projects()
        projects = [
            Project(name=proj[0], duration=proj[1], programming=proj[2], design=proj[3], marketing=proj[4])
            for proj in project_data
        ]
        print(f"Loaded projects: {projects}")
        return projects

    def load_researches(self):
        print("Loading researches from database...")
        research_data = self.storage.get_researches()
        researches = [
            Research(name=res[0], cost=res[1], duration=res[2], effect=res[3])
            for res in research_data
        ]
        print(f"Loaded researches: {researches}")
        return researches

    def open_project_selection(self):
        print("Opening project selection...")
        self.project_selector.open_project_selection()

    def start_selected_project(self, project, window):
        self.current_project = project
        self.project_manager.start_project()
        window.destroy()

    def resume_project(self):
        self.project_manager.resume_project()

    def stop_project(self):
        self.project_manager.stop_project()

    def train_developer(self):
        self.developer_manager.train_developer()

    def specialize_developer(self):
        self.developer_manager.specialize_developer()

    def start_research(self, research):
        self.research_manager.start_research(research)

    def auto_save_game(self):
        while True:
            time.sleep(self.AUTO_SAVE_INTERVAL)
            print("Auto-saving game...")
            self.storage.save_game(self)
            print("Game auto-saved.")

    def save_game(self):
        print("Saving game...")
        self.storage.save_game(self)
        print("Game saved.")

    def start_income_timer(self):
        self.income_timer = threading.Timer(1, self.generate_income)
        self.income_timer.daemon = True
        self.income_timer.start()

    def generate_income(self):
        total_salary = sum(dev.salary for dev in self.developers)
        income_per_second = (
            self.income_per_minute / 60
        )  # Convert income per minute to income per second
        salary_per_second = total_salary / (
            60 * 60
        )  # Convert salary per hour to salary per second
        self.balance += income_per_second
        self.gui.update_gui()
        self.income_timer = threading.Timer(1, self.generate_income)
        self.income_timer.daemon = True
        self.income_timer.start()

    def update_income_per_minute(self):
        total_salary = sum(dev.salary for dev in self.developers)
        project_income = (
            sum(project.programming for project in self.completed_projects_list) + sum(project.design for project in self.completed_projects_list) + sum(project.marketing for project in self.completed_projects_list) / 3 #Balanced Income/Minute
        )
        self.income_per_minute = project_income - (total_salary / 60)
        print(f"Updated income per minute: ${self.income_per_minute:.2f}")

    def display_developers_skills(self):
        print("Developers Skills:")
        for dev in self.developers:
            print(
                f"Name: {dev.name}, Programming: {dev.programming}, Design: {dev.design}, Marketing: {dev.marketing}"
            )

    def display_project_requirements(self):
        if self.current_project:
            print(f"Project Requirements - {self.current_project.name}:")
            print(f"Programming: {self.current_project.difficulty}")
            print(f"Design: {self.current_project.difficulty}")
            print(f"Marketing: {self.current_project.difficulty}")
        else:
            print("No project selected.")

    def run(self):
        self.gui.root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.run()
