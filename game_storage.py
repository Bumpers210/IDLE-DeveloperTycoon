import sqlite3
from contextlib import contextmanager
from models import Developer, Project


class GameStorage:
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    name TEXT,
                    duration INTEGER,
                    programming INTEGER,
                    design INTEGER,
                    marketing INTEGER
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS developers (
                    name TEXT,
                    skill INTEGER,
                    hunger INTEGER,
                    thirst INTEGER,
                    leisure INTEGER,
                    experience INTEGER,
                    programming INTEGER,
                    design INTEGER,
                    marketing INTEGER,
                    salary INTEGER
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS researches (
                    name TEXT,
                    cost INTEGER,
                    duration INTEGER,
                    effect TEXT
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS game_state (
                    id INTEGER PRIMARY KEY,
                    balance REAL,
                    income_per_minute REAL,
                    current_project_name TEXT,
                    remaining_project_time INTEGER,
                    training_cost REAL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS completed_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    duration INTEGER,
                    programming INTEGER,
                    design INTEGER,
                    marketing INTEGER
                )
            """
            )
            conn.commit()
            self.insert_default_projects_if_empty()
            self.insert_default_researches_if_empty()

    def insert_default_projects_if_empty(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM projects")
            if cursor.fetchone()[0] == 0:
                default_projects = [
                    ("Website", 30, 1, 1, 1),
                    ("Mobile App", 60, 2, 2, 2),
                    ("Game", 120, 3, 3, 3),
                    ("E-Commerce Platform", 180, 4, 4, 4),
                    ("AI Assistant", 240, 5, 5, 5),
                    ("Social Media Network", 300, 6, 6, 6),
                    ("Blockchain System", 360, 7, 7, 7),
                    ("Cloud Storage Service", 420, 8, 8, 8),
                    ("Video Streaming Service", 90, 3, 2, 1),
                    ("Weather Prediction System", 150, 4, 3, 2),
                    ("Fitness Tracking App", 60, 2, 2, 1),
                    ("Language Learning Platform", 200, 5, 4, 3),
                    ("Photo Editing Software", 180, 4, 4, 3),
                    ("Virtual Reality Game", 300, 6, 5, 4),
                    ("Online Education Portal", 240, 5, 5, 4),
                    ("Smart Home System", 210, 5, 4, 4),
                    ("Music Streaming Service", 150, 4, 3, 2),
                    ("Recipe Sharing App", 60, 2, 1, 1),
                    ("Personal Finance Manager", 180, 4, 3, 3),
                    ("Cryptocurrency Wallet", 300, 6, 6, 5),
                    ("Telemedicine Platform", 240, 5, 4, 5),
                    ("Remote Work Tool", 120, 3, 2, 3),
                    ("Event Management System", 210, 4, 4, 3),
                    ("Travel Booking System", 270, 5, 5, 4),
                    ("Content Management System", 180, 4, 3, 3),
                    ("Online Marketplace", 330, 6, 6, 5),
                    ("Inventory Management System", 150, 3, 3, 3),
                    ("Customer Support Chatbot", 90, 2, 2, 2),
                    ("Online Survey Tool", 120, 3, 2, 2),
                    ("Digital Publishing Platform", 270, 5, 5, 4),
                    ("Cybersecurity Solution", 360, 7, 6, 6),
                    ("Augmented Reality App", 300, 6, 5, 5),
                    ("Collaborative Whiteboard", 150, 4, 3, 3),
                    ("Voice Recognition System", 210, 5, 4, 4),
                    ("E-Learning Platform", 240, 5, 5, 4),
                    ("IoT Device Manager", 270, 6, 5, 5),
                    ("Health Monitoring System", 180, 4, 3, 4),
                    ("Automated Trading System", 360, 7, 7, 6),
                    ("Smart City Solution", 420, 8, 8, 7),
                    ("Interactive Storytelling App", 90, 3, 2, 2)
                ]

                cursor.executemany("INSERT INTO projects (name, duration, programming, design, marketing) VALUES (?, ?, ?, ?, ?)", default_projects)
                conn.commit()


    def insert_default_researches_if_empty(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM researches")
            if cursor.fetchone()[0] == 0:
                default_researches = [
                    ("Faster Development", 5000, 300, "Increase income"),
                    ("Cost Reduction", 7000, 400, "Decrease costs"),
                ]
                cursor.executemany(
                    "INSERT INTO researches (name, cost, duration, effect) VALUES (?, ?, ?, ?)",
                    default_researches,
                )
                conn.commit()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def get_projects(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, duration, programming, design, marketing FROM projects")
            return cursor.fetchall()

    def get_researches(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, cost, duration, effect FROM researches")
            return cursor.fetchall()

    def get_developers(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, skill, hunger, thirst, leisure, experience, programming, design, marketing, salary FROM developers"
            )
            return cursor.fetchall()

    def get_completed_projects(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, duration, programming, design, marketing FROM completed_projects")
            return cursor.fetchall()

    def save_game(self, game):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM developers")
            developers_data = [
                (
                    dev.name,
                    dev.skill,
                    dev.hunger,
                    dev.thirst,
                    dev.leisure,
                    dev.experience,
                    dev.programming,
                    dev.design,
                    dev.marketing,
                    dev.salary,
                )
                for dev in game.developers
            ]
            cursor.executemany(
                "INSERT INTO developers (name, skill, hunger, thirst, leisure, experience, programming, design, marketing, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                developers_data,
            )

            cursor.execute("DELETE FROM game_state")
            game_state_data = (
                1,
                game.balance,
                game.income_per_minute,
                game.current_project.name if game.current_project else None,
                game.remaining_project_time,
                game.training_cost,
            )
            cursor.execute(
                "INSERT INTO game_state (id, balance, income_per_minute, current_project_name, remaining_project_time, training_cost) VALUES (?, ?, ?, ?, ?, ?)",
                game_state_data,
            )

            cursor.execute("DELETE FROM completed_projects")
            completed_projects_data = [
                (proj.name, proj.duration, proj.programming, proj.design, proj.marketing)
                for proj in game.completed_projects_list
            ]
            cursor.executemany(
                "INSERT INTO completed_projects (name, duration, programming, design, marketing) VALUES (?, ?, ?, ?, ?)",
                completed_projects_data,
            )

            conn.commit()

    def load_game(self, game):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, skill, hunger, thirst, leisure, experience, programming, design, marketing, salary FROM developers"
            )
            developers_data = cursor.fetchall()
            game.developers = [Developer(*data) for data in developers_data]

            cursor.execute(
                "SELECT balance, income_per_minute, current_project_name, remaining_project_time, training_cost FROM game_state WHERE id = 1"
            )
            state = cursor.fetchone()
            if state:
                game.balance = state[0]
                game.income_per_minute = state[1]
                current_project_name = state[2]
                game.remaining_project_time = state[3]
                game.training_cost = state[4]

                if current_project_name:
                    for project in game.projects:
                        if project.name == current_project_name:
                            game.current_project = project
                            break

            cursor.execute("SELECT name, duration, programming, design, marketing FROM completed_projects")
            completed_projects_data = cursor.fetchall()
            game.completed_projects_list = [
                Project(name=proj[0], duration=proj[1], programming=proj[2], design=proj[3], marketing=proj[4])
                for proj in completed_projects_data
            ]
            game.completed_projects = len(game.completed_projects_list)

    @staticmethod
    def create_tables_if_not_exist():
        pass  # This method is kept for backward compatibility and is now part of initialize_database()
