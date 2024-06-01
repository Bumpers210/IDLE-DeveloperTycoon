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
from income import Income


class Game:
    AUTO_SAVE_INTERVAL = 60
    INITIAL_TRAINING_COST = 10

    def __init__(self):
        print("Initializing Game...")
        self.storage = GameStorage("game_data.db")
        self.income_per_minute = 0
        self.developers = Developer.load_developers_from_db(self.storage)
        self.projects = self.storage.load_projects()
        self.researches = self.storage.load_researches()
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
            target=self.storage.auto_save_game, args=(self,), daemon=True
        )
        self.auto_save_thread.start()

        self.event_manager = EventManager(self)
        self.project_selector = ProjectSelector(self)
        self.project_manager = ProjectManager(self)
        self.research_manager = ResearchManager(self)
        self.developer_manager = DeveloperManager(self)
        self.income = Income(self)

        self.gui = GameGUI(self)

        GameStorage.create_tables_if_not_exist()
        self.storage.load_game(self)

        if not self.developers:
            Developer.create_new_developer_start(self.developers)

        if self.current_project and self.remaining_project_time > 0:
            self.gui.update_project_timer(
                self.current_project.name,
                self.remaining_project_time,
                self.current_project.duration,
            )
            self.gui.enable_resume_button()

        self.income.update_income_per_minute()
        self.income.start_income_timer()
        self.gui.update_gui()
        self.event_manager.start_random_events()

        print("Game Initialized.")

    def display_developers_skills(self):
        print("Developers Skills:")
        for dev in self.developers:
            print(
                f"Name: {dev.name}, Programming: {dev.programming}, Design: {dev.design}, Marketing: {dev.marketing}"
            )

    def display_project_requirements(self):
        if self.current_project:
            print(f"Project Requirements - {self.current_project.name}:")
            print(f"Programming: {self.current_project.programming}")
            print(f"Design: {self.current_project.design}")
            print(f"Marketing: {self.current_project.marketing}")
        else:
            print("No project selected.")

    def run(self):
        self.gui.root.after(1000, self.event_manager.update_events)
        self.gui.root.mainloop()


if __name__ == "__main__":
    game = Game()
    game.run()
