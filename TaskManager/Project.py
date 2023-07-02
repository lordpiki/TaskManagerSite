import uuid
from datetime import date


class Project:
    def __init__(self, name, description, due_date, owner_id, project_id):
        self.project_id = project_id
        self.name = name
        self.owner_id = owner_id
        self.description = description
        self.due_date = due_date
        self.tasks = []

    def add_task(self, task):
        task.id = str(uuid.uuid4())
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_all_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def get_incomplete_tasks(self):
        return [task for task in self.tasks if not task.is_done]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.is_done]

    def get_today_tasks(self):
        return [task for task in self.tasks if date.today() in task.workDays]
