import random
import time


class EventManager:
    def __init__(self, game):
        self.game = game
        self.events = []

    def start_random_events(self):
        while True:
            time.sleep(
                random.randint(60, 120)
            )  # Random time between 60 und 120 Sekunden
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
        # Aktualisiere die Ereignisse in der GUI
        self.game.gui.update_events()

    def get_events(self):
        return self.events

    def update_project_delay(self, delay):
        delay_message = f"Project delay adjusted by {delay} seconds!"
        self.events.append(delay_message)
        self.game.gui.update_events()

    def update_project_start(self, project_name):
        update_message = f"Project started: {project_name}"
        self.events.append(update_message)
        self.game.gui.update_events()

    def update_project_complete(self, project_name):
        update_message = f"Project completed: {project_name}"
        self.events.append(update_message)
        self.game.gui.update_events()

    def update_project_stop(self):
        stop_message = f"Project stopped."
        self.events.append(stop_message)
        self.game.gui.update_events()
