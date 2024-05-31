import threading
import random
from tkinter import messagebox


class ProjectManager:
    def __init__(self, game):
        self.game = game

    def start_project(self):
        if self.game.current_project and not self.game.project_in_progress:
            print(f"Attempting to start project: {self.game.current_project.name}")
            if self.check_skills_for_project(self.game.current_project):
                project_name = self.game.current_project.name
                self.game.project_in_progress = True
                self.game.remaining_project_time = self.game.current_project.duration
                self.start_project_timer()
                print(f"Project started: {self.game.current_project.name}")
                self.game.event_manager.update_project_start(project_name)

    def check_skills_for_project(self, project):
        print(f"Checking skills for project: {project.name}")
        for developer in self.game.developers:
            if (
                developer.programming >= project.programming
                and developer.design >= project.design
                and developer.marketing >= project.marketing
            ):
                print(f"Skills are sufficient for project: {project.name}")
                return True
        print(f"Skills are not sufficient for project: {project.name}")
        return False

    def start_project_timer(self):
        self.game.gui.update_project_timer(
            self.game.current_project.name,
            self.game.remaining_project_time,
            self.game.current_project.duration,
        )
        self.game.project_timer = threading.Timer(1, self.update_project_time)
        self.game.project_timer.daemon = True
        self.game.project_timer.start()

    def resume_project(self):
        if self.game.current_project and not self.game.project_in_progress:
            print(f"Resuming project: {self.game.current_project.name}")
            self.game.project_in_progress = True
            self.start_project_timer()
            self.game.gui.disable_resume_button()
            print(f"Project resumed: {self.game.current_project.name}")

    def update_project_time(self):
        if self.game.project_in_progress:
            self.game.remaining_project_time -= 1
            self.game.gui.update_project_progress(
                self.game.current_project.duration, self.game.remaining_project_time
            )
            self.assign_exp_to_developers()
            if random.random() < 0.1:  # 10% chance for delay event
                self.handle_project_delay()
            if self.game.remaining_project_time <= 0:
                self.complete_project()
            else:
                self.game.project_timer = threading.Timer(1, self.update_project_time)
                self.game.project_timer.daemon = True
                self.game.project_timer.start()

    def handle_project_delay(self):
        delay = random.randint(-10, 10)  # Random delay between -10 to 10 seconds
        self.game.remaining_project_time += delay
        print(f"Project delay adjusted by {delay} seconds!")
        self.game.event_manager.update_project_delay(delay)

    def complete_project(self):
        if self.game.current_project:
            project_name = self.game.current_project.name
            print(f"Completing project: {self.game.current_project.name}")
            self.game.completed_projects += 1
            self.game.completed_projects_list.append(self.game.current_project)
            self.game.current_project = None
            self.game.project_in_progress = False
            self.game.remaining_project_time = 0
            self.game.update_income_per_minute()
            self.game.gui.project_completed()
            self.game.gui.update_gui()
            print("Project completed.")
            self.game.event_manager.update_project_complete(project_name)

    def stop_project(self):
        if self.game.project_in_progress:
            print("Project stopped.")
            self.game.project_in_progress = False
            self.game.current_project = None
            self.game.remaining_project_time = 0
            self.game.gui.project_stopped()
            self.game.gui.update_gui()
            self.game.event_manager.update_project_stop()

    def assign_exp_to_developers(self):
        if self.game.current_project:
            difficulty = (
                self.game.current_project.programming
                + self.game.current_project.design
                + self.game.current_project.marketing
            )
            exp_per_second = (difficulty * 0.5) / 60
            for developer in self.game.developers:
                developer.gain_exp(exp_per_second)
            self.game.gui.update_developers_skills()
