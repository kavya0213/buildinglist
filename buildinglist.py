import json
import os

class Task:
    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = False  # Initially, task is not completed

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.title} - {self.priority} - Due: {self.due_date} - Status: {status}"

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(task_dict):
        return Task(task_dict['title'], task_dict['description'], task_dict['due_date'],
                    task_dict['priority'])

class TodoList:
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                tasks = json.load(f)
                self.tasks = [Task.from_dict(task) for task in tasks]

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            tasks = [task.to_dict() for task in self.tasks]
            json.dump(tasks, f, indent=4)

    def add_task(self, title, description, due_date, priority):
        new_task = Task(title, description, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def delete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                self.save_tasks()
                return
        print("Task not found.")

    def update_task(self, title, **kwargs):
        for task in self.tasks:
            if task.title == title:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                self.save_tasks()
                return
        print("Task not found.")

    def view_tasks(self):
        for task in self.tasks:
            print(task)

    def mark_completed(self, title):
        for task in self.tasks:
            if task.title == title:
                task.completed = True
                self.save_tasks()
                return
        print("Task not found.")

    def filter_by_due_date(self, due_date):
        filtered_tasks = [task for task in self.tasks if task.due_date == due_date]
        if filtered_tasks:
            for task in filtered_tasks:
                print(task)
        else:
            print("No tasks found for the given due date.")

    def filter_by_priority(self, priority):
        filtered_tasks = [task for task in self.tasks if task.priority == priority]
        if filtered_tasks:
            for task in filtered_tasks:
                print(task)
        else:
            print("No tasks found for the given priority.")

# Example usage:
def main():
    todo_list = TodoList("tasks.json")

    while True:
        print("\n===== TO-DO LIST MENU =====")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View All Tasks")
        print("5. Mark Task as Complete")
        print("6. Filter Tasks by Due Date")
        print("7. Filter Tasks by Priority")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority (Low/Medium/High): ")
            todo_list.add_task(title, description, due_date, priority)

        elif choice == '2':
            title = input("Enter title of task to delete: ")
            todo_list.delete_task(title)

        elif choice == '3':
            title = input("Enter title of task to update: ")
            description = input("Enter updated description (press Enter to keep current): ")
            due_date = input("Enter updated due date (YYYY-MM-DD) (press Enter to keep current): ")
            priority = input("Enter updated priority (Low/Medium/High) (press Enter to keep current): ")

            update_dict = {}
            if description:
                update_dict['description'] = description
            if due_date:
                update_dict['due_date'] = due_date
            if priority:
                update_dict['priority'] = priority

            todo_list.update_task(title, **update_dict)

        elif choice == '4':
            print("\n===== ALL TASKS =====")
            todo_list.view_tasks()

        elif choice == '5':
            title = input("Enter title of task to mark as complete: ")
            todo_list.mark_completed(title)

        elif choice == '6':
            due_date = input("Enter due date to filter tasks (YYYY-MM-DD): ")
            todo_list.filter_by_due_date(due_date)

        elif choice == '7':
            priority = input("Enter priority to filter tasks (Low/Medium/High): ")
            todo_list.filter_by_priority(priority)

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 8.")

if __name__ == "__main__":
    main()
