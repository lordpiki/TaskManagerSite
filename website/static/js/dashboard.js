document.addEventListener('DOMContentLoaded', function () {
  const projectList = document.querySelectorAll('.project-list li');
  const projectName = document.getElementById('selected-project-name');
  const projectTasks = document.getElementById('task-list');
  const addTaskButton = document.getElementById('add-task-button');

  projectList.forEach(function (project) {
    project.addEventListener('click', function () {
      // Remove 'selected' class from all projects
      projectList.forEach(function (item) {
        item.classList.remove('selected');
      });

      // Add 'selected' class to clicked project
      this.classList.add('selected');

      // Update the project name
      projectName.textContent = this.textContent;

      // Clear the existing task list
      projectTasks.innerHTML = '';

      // Fetch tasks for the selected project from the server
      const projectId = this.getAttribute('data-project-id');
      getTasks(projectId);
    });
  });

  // Function to fetch tasks for a project
  function getTasks(projectId) {
    fetch(`/get_tasks/${projectId}`)
      .then(response => response.json())
      .then(tasks => {
        // Create and append task items
        tasks.forEach(task => {
          const taskItem = createTaskItem(task);
          projectTasks.appendChild(taskItem);
        });
      })
      .catch(error => console.error(error));
  }

  // Function to create a task item element
  function createTaskItem(task) {
    const taskItem = document.createElement('li');
    taskItem.textContent = `Name: ${task.name}, Description: ${task.description}, Priority: ${task.priority}`;
    return taskItem;
  }

  addTaskButton.addEventListener('click', function () {
    // TODO: Implement logic for adding a new task
  });
});



const optionMenu = document.querySelector(".select-menu"),
       selectBtn = optionMenu.querySelector(".select-btn"),
       options = optionMenu.querySelectorAll(".option"),
       sBtn_text = optionMenu.querySelector(".sBtn-text");

selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));

options.forEach(option =>{
    option.addEventListener("click", ()=>{
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;

        optionMenu.classList.remove("active");
    });
});