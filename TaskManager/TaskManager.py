#from User import User
#from Task import Task
#from Project import Project
from .SQLiteManager import SQLiteManager


class TaskManager:
    def __init__(self):
        self.db_manager = SQLiteManager("database.db")

    def signup(self, username, password):
        # Check if user already exists
        existing_user = self.db_manager.get_user_by_credentials(username, password)
        if existing_user:
            return None

        # Create a new user
        return self.db_manager.signup(username, password)

    def login(self, username, password):
        return self.db_manager.get_user_by_credentials(username, password)

    def get_user(self, user_id):
        return self.db_manager.get_user(user_id)

    def get_user_projects(self, user_id):
        user = self.db_manager.get_user(user_id)
        if user:
            return user.get_all_projects()
        return []

    def add_project(self, name, owner_id, description, due_date=None):
        return self.db_manager.add_project(name, owner_id, description, due_date)

    def get_project(self, project_id):
        return self.db_manager.get_project(project_id)

    def get_project_tasks(self, project_id):
        return self.db_manager.get_project_tasks(project_id)

    def get_user_tasks(self, user_id):
        user = self.db_manager.get_user(user_id)
        if user:
            tasks = []
            projects = user.get_all_projects()
            for project in projects:
                tasks.extend(project.get_all_tasks())
            return tasks
        return []

    def add_task(self, name, project_id, color, description, priority, is_done=False):
        project = self.db_manager.get_project(project_id)
        if project:
            self.db_manager.add_task(name, project_id, color, description, priority, is_done)

    # Add other methods for retrieving tasks, categories, etc.

