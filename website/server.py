from flask import Flask, render_template, request, redirect, session, jsonify
from TaskManager.TaskManager import TaskManager

app = Flask(__name__)
app.secret_key = "your-secret-key"

task_manager = TaskManager()

@app.route("/")
def index():
    return redirect("/login")

def task_to_dict(task):
    return {
        'name': task.name,
        'description': task.description,
        'priority': task.priority,
        # Add more attributes as needed
    }

@app.route('/get_tasks/<project_id>')
def get_tasks(project_id):
    # Call task_manager.get_project_tasks(project_id) to fetch tasks
    tasks = task_manager.get_project_tasks(project_id)

    # Convert tasks to JSON-serializable format
    serialized_tasks = [task_to_dict(task) for task in tasks]
    print(project_id)

    # Return tasks as JSON response
    return jsonify(serialized_tasks)

@app.route("/project/<string:project_id>/add_task", methods=["POST"])
def add_task(project_id):
    if "user_id" in session:
        user_id = session["user_id"]
        user = task_manager.get_user(user_id)
        if user:
            task_name = request.form["task_name"]
            task_color = request.form["task_color"]
            task_description = request.form["task_description"]
            task_priority = request.form["task_priority"]

            task_manager.add_task(task_name, project_id, task_color, task_description, task_priority)

            return redirect("/projects/" + project_id)  # Redirect to the project page

    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = task_manager.signup(username, password)
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("signup.html", error="Username already exists.")
    return render_template("signup.html", error="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = task_manager.login(username, password)
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html", error="")

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        user = task_manager.get_user(user_id)
        if user:
            projects = task_manager.get_user_projects(user_id)
            return render_template("dashboard.html", user=user, projects=projects)
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

@app.route("/projects/<project_id>")
def project_details(project_id):
    if "user_id" in session:
        user_id = session["user_id"]
        user = task_manager.get_user(user_id)
        if user:
            project = task_manager.get_project(project_id)
            if project:
                tasks = task_manager.get_project_tasks(project_id)
                return render_template("project.html", project=project, tasks=tasks)
    return redirect("/login")

@app.route("/projects/new", methods=["GET", "POST"])
def create_project():
    if "user_id" in session:
        user_id = session["user_id"]
        user = task_manager.get_user(user_id)
        if user:
            if request.method == "POST":
                name = request.form["name"]
                description = request.form["description"]
                task_manager.add_project(name, user_id, description)
                return redirect("/dashboard")
            return render_template("create_project.html")
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
