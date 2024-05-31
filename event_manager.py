import random
import time
import threading
import tkinter as tk

class EventManager:
    def __init__(self, game):
        self.game = game
        self.events = []

    def update_events(self):
        events = self.get_events()
        self.game.gui.event_history_text.config(state=tk.NORMAL)
        self.game.gui.event_history_text.delete("1.0", tk.END)
        for event in reversed(events):  # Reverse the order to show the latest events at the top
            self.game.gui.event_history_text.insert("1.0", event + "\n")
        self.game.gui.event_history_text.config(state=tk.DISABLED)
        self.game.gui.root.after(1000, self.update_events)

    def start_random_events(self):
        threading.Thread(target=self._random_events_loop, daemon=True).start()

    def _random_events_loop(self):
        while True:
            time.sleep(random.randint(60, 120))  # Random time between 60 and 120 seconds
            self.trigger_random_event()

    def trigger_random_event(self):
        event = random.choice(["bonus", "penalty"])
        if event == "bonus":
            bonus = random.randint(10, 50)
            self.game.balance += bonus
            event_message = f"Received a bonus of ${bonus}"
            self.events.append(event_message)
            print(f"Random event: {event_message}")
        elif event == "penalty":
            penalty = random.randint(10, 50)
            self.game.balance -= penalty
            event_message = f"Incurred a penalty of ${penalty}"
            self.events.append(event_message)
            print(f"Random event: {event_message}")
        self.update_events()

    def get_events(self):
        return self.events

    def update_project_delay(self, delay):
        delay_message = f"Project delay adjusted by {delay} seconds!"
        self.events.append(delay_message)
        self.update_events()

    def update_project_start(self, project_name):
        update_message = f"Project started: {project_name}"
        self.events.append(update_message)
        self.update_events()

    def update_project_complete(self, project_name):
        update_message = f"Project completed: {project_name}"
        self.events.append(update_message)
        self.update_events()

    def update_project_stop(self):
        stop_message = f"Project stopped."
        self.events.append(stop_message)
        self.update_events()
