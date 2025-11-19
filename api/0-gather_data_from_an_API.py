#!/usr/bin/python3
"""
Script that fetches an employee's TODO list progress from a REST API
and displays it in the specified format.
"""

import sys

import requests


def get_employee_todo_progress(employee_id: int) -> None:
    """
    Fetch and display the TODO list progress for a given employee ID.

    Args:
        employee_id (int): The ID of the employee
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee details
    user_response = requests.get(f"{base_url}/users/{employee_id}")
    if user_response.status_code != 200:
        print("Employee not found")
        return

    user = user_response.json()
    employee_name = user.get("name")

    # Fetch employee's todos
    todos_response = requests.get(f"{base_url}/todos", params={"userId": employee_id})
    todos = todos_response.json()

    # Count completed and total tasks
    completed_tasks = [task for task in todos if task.get("completed")]
    number_of_done_tasks = len(completed_tasks)
    total_number_of_tasks = len(todos)

    # Display progress
    print(
        f"Employee {employee_name} is done with tasks("
        f"{number_of_done_tasks}/{total_number_of_tasks}):"
    )

    # Display titles of completed tasks for indentation
    for task in completed_tasks:
        print(f"\t {task.get('title')}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    get_employee_todo_progress(emp_id)
