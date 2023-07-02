from enum import Enum


class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NO = "None"


class Task:
    def __init__(self, task_id, name, description,  workDays=None, project_id="None", color="Gray", priority=Priority.NO.value, is_done=False):
        self.name = name
        self.project_id = project_id
        self.color = color
        self.description = description
        self.priority = priority
        self.is_done = is_done
        self.id = task_id
        self.workDays = workDays or []

    def mark_as_done(self):
        self.is_done = True

    def mark_as_undone(self):
        self.is_done = False

    def add_work_day(self, workDay):
        self.workDays.append(workDay)
