import tkinter as tk
from tkinter import ttk, messagebox


class GameGUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Developer Tycoon")
        self.create_gui()
        self.update_events()  # Start the event update loop

    def create_gui(self):
        # Main frame to hold left and right sections
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for info, control and project frames
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create frames for better organization
        self.info_frame = tk.Frame(
            self.left_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10
        )
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.control_frame = tk.Frame(
            self.left_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10
        )
        self.control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.project_frame = tk.Frame(
            self.left_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10
        )
        self.project_frame.pack(fill=tk.X, padx=10, pady=10)

        # Configure grid layout for control_frame to ensure equal button sizes
        for i in range(6):
            self.control_frame.grid_columnconfigure(i, weight=1, uniform="button")

        # Right side: Live Event History
        self.event_history_frame = tk.Frame(
            self.main_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10
        )
        self.event_history_frame.pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.RIGHT
        )

        self.event_history_label = tk.Label(
            self.event_history_frame, text="Event History", font=("Arial", 12)
        )
        self.event_history_label.pack(pady=5)

        self.event_history_text = tk.Text(self.event_history_frame, height=20, width=50)
        self.event_history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Info Labels
        self.label_balance = tk.Label(
            self.info_frame, text="Balance: $0.00", font=("Arial", 12)
        )
        self.label_balance.grid(row=0, column=0, padx=10, pady=5)

        self.label_completed_projects = tk.Label(
            self.info_frame, text="Completed Projects: 0", font=("Arial", 12)
        )
        self.label_completed_projects.grid(row=0, column=1, padx=10, pady=5)

        self.label_income_per_minute = tk.Label(
            self.info_frame, text="Income/Minute: $0.00", font=("Arial", 12)
        )
        self.label_income_per_minute.grid(row=0, column=2, padx=10, pady=5)

        self.label_training_cost = tk.Label(
            self.info_frame, text="Training Cost: $10.00", font=("Arial", 12)
        )
        self.label_training_cost.grid(row=0, column=3, padx=10, pady=5)

        # Developers Skills Label
        self.label_developers_skills = tk.Label(
            self.info_frame, text="", font=("Arial", 10)
        )
        self.label_developers_skills.grid(row=1, columnspan=4, padx=10, pady=5)

        # Project Requirements Label
        self.label_project_requirements = tk.Label(
            self.info_frame, text="", font=("Arial", 10)
        )
        self.label_project_requirements.grid(row=2, columnspan=4, padx=10, pady=5)

        # Project Progress
        self.label_project_duration = tk.Label(
            self.project_frame, text="", font=("Arial", 12)
        )
        self.label_project_duration.pack(pady=5)

        self.progress_project = ttk.Progressbar(
            self.project_frame, length=400, mode="determinate"
        )
        self.progress_project.pack(pady=5)

        self.label_project_delay = tk.Label(
            self.project_frame, text="", font=("Arial", 10)
        )
        self.label_project_delay.pack(pady=5)

        self.label_project_update = tk.Label(
            self.project_frame, text="", font=("Arial", 10)
        )
        self.label_project_update.pack(pady=5)

        # Control Buttons
        self.button_start_project = tk.Button(
            self.control_frame,
            text="Start Project",
            command=self.game.open_project_selection,
            font=("Arial", 10),
        )
        self.button_start_project.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.button_stop_project = tk.Button(
            self.control_frame,
            text="Stop Project",
            command=self.game.stop_project,
            state=tk.DISABLED,
            font=("Arial", 10),
        )
        self.button_stop_project.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.button_resume_project = tk.Button(
            self.control_frame,
            text="Resume Project",
            command=self.game.resume_project,
            state=tk.DISABLED,
            font=("Arial", 10),
        )
        self.button_resume_project.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.button_train = tk.Button(
            self.control_frame,
            text="Train Developer",
            command=self.game.train_developer,
            font=("Arial", 10),
        )
        self.button_train.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.button_start_research = tk.Button(
            self.control_frame,
            text="Start Research",
            command=self.open_research_selection,
            font=("Arial", 10),
        )
        self.button_start_research.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        self.button_save = tk.Button(
            self.control_frame,
            text="Save Game",
            command=self.game.save_game,
            font=("Arial", 10),
        )
        self.button_save.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

        self.button_quit = tk.Button(
            self.control_frame,
            text="Quit Game",
            command=self.quit_game,
            font=("Arial", 10),
        )
        self.button_quit.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.update_gui()

    def quit_game(self):
        print("Quitting game...")
        self.game.save_game()
        self.root.destroy()

    def update_gui(self):
        self.label_balance.config(text=f"Balance: ${self.game.balance:.2f}")
        self.label_completed_projects.config(
            text=f"Completed Projects: {self.game.completed_projects}"
        )
        self.label_income_per_minute.config(
            text=f"Income/Minute: ${self.game.income_per_minute:.2f}"
        )
        self.label_training_cost.config(
            text=f"Training Cost: ${self.game.training_cost:.2f}"
        )
        self.update_developers_skills()
        self.update_project_requirements()

    def update_project_timer(self, project_name, remaining_time, total_duration):
        self.label_project_duration.config(
            text=f"Working on: {project_name} - Remaining Time: {remaining_time} seconds"
        )
        self.progress_project["maximum"] = total_duration
        self.progress_project["value"] = total_duration - remaining_time
        self.button_stop_project.config(state=tk.NORMAL)

    def update_project_progress(self, total_duration, remaining_time):
        self.progress_project["value"] = total_duration - remaining_time
        self.label_project_duration.config(
            text=f"Working on: {self.game.current_project.name} - Remaining Time: {remaining_time} seconds"
        )

    def project_completed(self):
        self.label_project_duration.config(text="Project Completed!")
        self.progress_project["value"] = 0
        self.button_stop_project.config(state=tk.DISABLED)
        self.button_resume_project.config(state=tk.DISABLED)

    def project_stopped(self):
        self.label_project_duration.config(text="Project Stopped!")
        self.progress_project["value"] = 0
        self.button_stop_project.config(state=tk.DISABLED)
        self.button_resume_project.config(state=tk.DISABLED)

    def update_developers_skills(self):
        developers_skills = "Developers Skills:\n"
        for dev in self.game.developers:
            developers_skills += f"{dev.name}: Skill {dev.skill}, Programming {dev.programming}, Design {dev.design}, Marketing {dev.marketing}, EXP: {dev.experience:.2f}\n"
        self.label_developers_skills.config(text=developers_skills)

    def update_project_requirements(self):
        if self.game.current_project:
            project_requirements = (
                f"Project Requirements - {self.game.current_project.name}:\n"
                f"Programming: {self.game.current_project.programming}\n"
                f"Design: {self.game.current_project.design}\n"
                f"Marketing: {self.game.current_project.marketing}"
            )
        else:
            project_requirements = "No project selected."
        self.label_project_requirements.config(text=project_requirements)

    def open_research_selection(self):
        research_window = tk.Toplevel(self.root)
        research_window.title("Select Research")

        label = tk.Label(research_window, text="Select a research to start:")
        label.pack(padx=10, pady=10)

        listbox = tk.Listbox(research_window)
        listbox.pack(padx=10, pady=10)

        for res in self.game.researches:
            listbox.insert(tk.END, res.name)

        def start_research():
            selected_research_index = listbox.curselection()
            if selected_research_index:
                selected_research = self.game.researches[selected_research_index[0]]
                self.game.start_research(selected_research)
                research_window.destroy()

        button = tk.Button(
            research_window, text="Start Research", command=start_research
        )
        button.pack(padx=10, pady=10)

    def enable_resume_button(self):
        self.button_resume_project.config(state=tk.NORMAL)

    def update_events(self):
        events = self.game.event_manager.get_events()
        self.event_history_text.config(state=tk.NORMAL)
        # Lösche den gesamten Text nur einmal
        self.event_history_text.delete("1.0", tk.END)
        for event in events:
            # Füge jedes Ereignis am Anfang ein
            self.event_history_text.insert("1.0", event + "\n")
        self.event_history_text.config(state=tk.DISABLED)
        self.root.after(1000, self.update_events)

