from .User import User
from .Task import Task
from .Project import Project

import uuid
import sqlite3


class SQLiteManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Create Task table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Task (
                                id TEXT PRIMARY KEY,
                                name TEXT,
                                project_id TEXT,
                                color TEXT,
                                description TEXT,
                                category TEXT,
                                priority TEXT DEFAULT 'None',
                                is_done INTEGER
                            )''')


            # Create Project table
            cursor.execute('''CREATE TABLE IF NOT EXISTS Project (
                                id TEXT PRIMARY KEY,
                                owner_id TEXT,
                                name TEXT,
                                description TEXT,
                                due_date TEXT DEFAULT NULL,
                                FOREIGN KEY (owner_id) REFERENCES User (id)
                            )''')

            # Create User table
            cursor.execute('''CREATE TABLE IF NOT EXISTS User (
                                id TEXT PRIMARY KEY,
                                username TEXT,
                                password TEXT
                            )''')

            conn.commit()

    def get_user_by_credentials(self, username, password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
            row = cursor.fetchone()

            if row:
                return self.get_user(row[0])

            return None

    def get_user_id(self, name):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM User WHERE username = ?", (name,))
            user_id = cursor.fetchone()
            return user_id[0] if user_id else None

    def get_project(self, project_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Project WHERE id = ?", (project_id,))
            project_data = cursor.fetchone()

            if project_data:
                project_id, owner_id, name, description, due_date = project_data
                project = Project(name, description, due_date, owner_id, project_id)
                return project

            return None

    def get_project_tasks(self, project_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Task WHERE project_id = ?", (project_id,))
            task_data = cursor.fetchall()
            tasks = []
            for task in task_data:
                task_id, name, project_id, color, description, category, priority, is_done = task
                task_obj = Task(task_id=task_id, name=name, description=description,
                                priority=priority, is_done=is_done, project_id=project_id)
                tasks.append(task_obj)
            return tasks

    def get_user(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM User WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()

            if user_data:
                username, password = user_data[1], user_data[2]
                user = User(username, password, user_id)
                user.projects = self.get_user_projects(user.id)
                return user
            return None

    def get_user_tasks(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Task WHERE project_id IN (SELECT id FROM Project WHERE owner_id = ?)",
                           (user_id,))
            task_data = cursor.fetchall()
            tasks = []
            for task in task_data:
                task_id, name, project_id, color, description, priority, is_done = task[0], task[1], task[2], \
                                                                                             task[3], task[4], task[5], \
                                                                                             task[6]
                task_obj = Task(name, description, color, priority, is_done)
                task_obj.id = task_id
                task_obj.project_id = project_id
                tasks.append(task_obj)
            return tasks

    def get_user_projects(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Project WHERE owner_id = ?", (user_id,))
            project_data = cursor.fetchall()
            projects = []
            for project in project_data:
                project_id, owner_id, name, description, due_date = project[0], project[1], project[2], project[3], \
                                                                    project[4]
                project_obj = Project(name, description, due_date, owner_id, project_id)
                project_obj.tasks = self.get_project_tasks(project_id)
                projects.append(project_obj)
            return projects

    def login(self, name, password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM User WHERE username = ? AND password = ?", (name, password))
            user_id = cursor.fetchone()
            if user_id:
                return self.get_user(user_id[0])
            return None

    def signup(self, name, password):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            user_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO User (id, username, password) VALUES (?, ?, ?)", (user_id, name, password))
            conn.commit()
            return self.get_user(user_id)

    def add_task(self, name, project_id, color, description, priority, is_done=False):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            task_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO Task (id, name, project_id, color, description, priority, is_done) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (task_id, name, project_id, color, description, priority, is_done))
            conn.commit()

    def add_project(self, name, owner_id, description, due_date=None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            project_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO Project (id, owner_id, name, description, due_date) VALUES (?, ?, ?, ?, ?)",
                           (project_id, owner_id, name, description, due_date))
            conn.commit()

    def add_category(self, name, color):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Category (name, color) VALUES (?, ?)", (name, color))
            conn.commit()

    def _get_connection(self):
        return sqlite3.connect(self.db_file)


# Usage example:
if __name__ == '__main__':
    db_manager = SQLiteManager('task_manager.db')
    db_manager.create_tables()
