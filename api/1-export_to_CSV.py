#!/usr/bin/python3
"""
Fetch employee TODO list data from JSONPlaceholder API
and export all tasks (completed or not) to a CSV file: USER_ID.csv
"""

import csv
import requests
import sys


def export_employee_tasks_to_csv(employee_id: int) -> None:
    """
    Export all tasks owned by the given employee to a CSV file.

    CSV format:
        "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
    File name: USER_ID.csv
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Get employee info
    user_resp = requests.get(f"{base_url}/users/{employee_id}")
    if user_resp.status_code != 200:
        print(f"Employee with ID {employee_id} not found")
        return

    user_data = user_resp.json()
    user_id = user_data.get("id")
    username = user_data.get("name")

    # Get all todos for this employee
    todos_resp = requests.get(f"{base_url}/todos",
                              params={"userId": employee_id})
    todos = todos_resp.json()

    # Prepare CSV file
    filename = f"{user_id}.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        for task in todos:
            writer.writerow([
                user_id,
                username,
                task.get("completed"),
                task.get("title")
            ])

    print(f"Data exported successfully to {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./1-export_to_CSV.py <employee_id>")
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer")
        sys.exit(1)

    export_employee_tasks_to_csv(emp_id)
