class User:
    def __init__(self, username, password, user_id):
        self.id = user_id
        self.username = username
        self.password = password
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def remove_project(self, project):
        self.projects.remove(project)

    def get_all_projects(self):
        return self.projects

    def get_todays_task(self):
        return [project.get_today_tasks() for project in self.projects]
