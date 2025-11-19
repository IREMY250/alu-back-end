#!/usr/bin/python3
"""
Script that fetches an employee's TODO list progress from a REST API
and displays it in the specified format.
"""

import requests
import sys


def get_employee_todo_progress(employee_id: int) -> None:
    """
    Fetch and display the TODO list progress for a given employee ID.

    Args:
        employee_id (int): The ID of the employee
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch employee details
    user_resp = requests.get(f"{base_url}/users/{employee_id}")
    if user_resp.status_code != 200:
        print("Employee not found")
        return

    employee_name = user_resp.json().get("name")

    # Fetch employee's todos
    todor = requests.get(f"{base_url}/todos", params={"userId": employee_id})
    todos = todor.json()

    # Calculate completed tasks
    completed = [t for t in todos if t.get("completed")]
    done = len(completed)
    total = len(todos)

    # First line
    print(f"Employee {employee_name} is done with tasks({done}/{total}):")

    # Completed task titles (with exactly one tab and one space before title)
    for task in completed:
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
