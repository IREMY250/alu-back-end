#!/usr/bin/python3
"""
Export employee TODO list to CSV format using the correct username field.
File: USER_ID.csv
Format: "USER_ID","USERNAME","TASK_COMPLETED_STATUS","TASK_TITLE"
"""

import csv
import requests
import sys


def export_to_csv(employee_id: int) -> None:
    """
    Fetch employee tasks and export them to a CSV file.
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Fetch user data
    user_response = requests.get(f"{base_url}/users/{employee_id}")
    if user_response.status_code != 200:
        return

    user = user_response.json()
    user_id = user.get("id")
    username = user.get("username")

    # Fetch all tasks for this user
    todos_response = requests.get(f"{base_url}/todos",
                                  params={"userId": employee_id})
    todos = todos_response.json()

    # Write to CSV
    filename = f"{user_id}.csv"
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for task in todos:
            writer.writerow([
                user_id,
                username,
                task.get("completed"),
                task.get("title")
            ])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        sys.exit(1)

    export_to_csv(emp_id)
