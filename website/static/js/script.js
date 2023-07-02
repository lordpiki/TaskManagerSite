document.addEventListener('DOMContentLoaded', function() {
    const addTaskButton = document.getElementById('add-task-button');
    const addTaskForm = document.getElementById('add-task-form');

    addTaskButton.addEventListener('click', function() {
        addTaskForm.classList.toggle('hidden');
    });
});
