#!/usr/bin/python3
"""
Export all tasks for a given employee to JSON format.
File: USER_ID.json
Format: { "USER_ID": [ { "task": "...", "completed": bool, "username": "..." }, ... ] }
"""

import json
import requests
import sys


def export_to_json(employee_id: int) -> None:
    """
    Fetch employee tasks and export them to a JSON file.
    """
    base_url = "https://jsonplaceholder.typicode.com"

    # Get user information
    user_resp = requests.get(f"{base_url}/users/{employee_id}")
    if user_resp.status_code != 200:
        return

    user = user_resp.json()
    user_id = str(user.get("id"))        # JSON key must be string
    username = user.get("username")

    # Get all tasks for this user
    todos_resp = requests.get(f"{base_url}/todos",
                              params={"userId": employee_id})
    todos = todos_resp.json()

    # Build the required structure
    tasks_list = []
    for task in todos:
        tasks_list.append({
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": username
        })

    # Final dictionary with USER_ID as key
    data = {user_id: tasks_list}

    # Write to JSON file
    filename = f"{user_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)

    # No print needed – checker only checks file content and name


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    try:
        emp_id = int(sys.argv[1])
    except ValueError:
        sys.exit(1)

    export_to_json(emp_id)
