import random
import json


class Developer:
    def __init__(
        self,
        name,
        skill,
        hunger,
        thirst,
        leisure,
        experience,
        programming,
        design,
        marketing,
        salary,
    ):
        self.name = name
        self.skill = skill
        self.hunger = hunger
        self.thirst = thirst
        self.leisure = leisure
        self.experience = experience
        self.programming = programming
        self.design = design
        self.marketing = marketing
        self.salary = salary
        self.specialization = None

    def train(self, skill_type):
        if skill_type == "programming":
            self.programming += 1
        elif skill_type == "design":
            self.design += 1
        elif skill_type == "marketing":
            self.marketing += 1
        self.experience += 1

    def specialize(self, specialization):
        self.specialization = specialization
        if specialization == "Frontend":
            self.programming += 2
        elif specialization == "Backend":
            self.programming += 2
        elif specialization == "Fullstack":
            self.programming += 1
            self.design += 1

    def gain_exp(self, amount):
        self.experience += amount
        if self.experience >= 100:
            self.experience = 0
            self.increase_skill()

    def increase_skill(self):
        # Simple logic to increase the skill with the lowest value
        skill = {'skill': self.skill}
        min_skill = min(skill, key=skill.get)
        setattr(self, min_skill, getattr(self, min_skill) + 1)
        print(f"{self.name}'s {min_skill} skill increased to {getattr(self, min_skill)}")

    @classmethod
    def create_new_developer(cls, developers):
        name = f"Developer{len(developers) + 1}"
        skill = 0
        hunger = random.randint(65, 100)
        thirst = random.randint(65, 100)
        leisure = random.randint(0, 33)
        programming = random.randint(1, 3)
        design = random.randint(1, 3)
        marketing = random.randint(1, 3)
        salary = random.randint(500, 1500)
        new_dev = cls(
            name,
            skill,
            hunger,
            thirst,
            leisure,
            0,
            programming,
            design,
            marketing,
            salary,
        )
        developers.append(new_dev)

    @staticmethod
    def load_developers_from_db(storage):
        developers_data = storage.get_developers()
        developers = [Developer(*data) for data in developers_data]
        return developers


class Project:
    def __init__(self, name, duration, programming, design, marketing):
        self.name = name
        self.duration = duration
        self.programming = programming
        self.design = design
        self.marketing = marketing


class Research:
    def __init__(self, name, cost, duration, effect):
        self.name = name
        self.cost = cost
        self.duration = duration
        self.effect = effect

    def apply(self, game):
        if self.effect == "Increase income":
            game.income_per_minute += 10
        elif self.effect == "Decrease costs":
            for dev in game.developers:
                dev.salary = max(1000, dev.salary - 200)
