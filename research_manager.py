import threading
import tkinter as tk

class ResearchManager:
    def __init__(self, game):
        self.game = game
        
    def open_research_selection(self):
        research_window = tk.Toplevel(self.game.gui.root)
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
                self.start_research(selected_research)
                research_window.destroy()

        button = tk.Button(
            research_window, text="Start Research", command=start_research
        )
        button.pack(padx=10, pady=10)

    def start_research(self, research):
        if self.game.balance >= research.cost:
            self.game.balance -= research.cost
            self.game.current_research = research
            self.game.remaining_research_time = research.duration
            self.start_research_timer()
            print(f"Started research: {research.name}")
        else:
            print("Not enough balance to start research.")

    def start_research_timer(self):
        self.game.research_timer = threading.Timer(1, self.update_research_time)
        self.game.research_timer.daemon = True
        self.game.research_timer.start()

    def update_research_time(self):
        if self.game.current_research:
            self.game.remaining_research_time -= 1
            if self.game.remaining_research_time <= 0:
                self.complete_research()
            else:
                self.game.research_timer = threading.Timer(1, self.update_research_time)
                self.game.research_timer.daemon = True
                self.game.research_timer.start()

    def complete_research(self):
        if self.game.current_research:
            print(f"Completed research: {self.game.current_research.name}")
            self.game.current_research.apply(self.game)
            self.game.current_research = None
            self.game.remaining_research_time = 0
            self.game.gui.update_gui()
