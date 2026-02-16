"""
Mega Python Program: Personal Productivity & Task Analytics System
Author: Random Big Python Code 😄
Description:
- User management
- Task creation & tracking
- Priority-based scheduling
- Productivity analytics
- File-based persistence
- Simulation mode
"""

import json
import os
import uuid
import datetime
import random
from collections import defaultdict

DATA_FILE = "productivity_data.json"


# -------------------- UTILITIES --------------------

def generate_id():
    return str(uuid.uuid4())[:8]


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# -------------------- DATA HANDLING --------------------

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.data = {
            "users": {},
            "tasks": {}
        }
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def reset(self):
        self.data = {"users": {}, "tasks": {}}
        self.save()


db = Database(DATA_FILE)


# -------------------- USER MANAGEMENT --------------------

class User:
    def __init__(self, name, email):
        self.id = generate_id()
        self.name = name
        self.email = email
        self.created_at = current_time()

    def to_dict(self):
        return self.__dict__


def create_user():
    name = input("Enter name: ")
    email = input("Enter email: ")
    user = User(name, email)
    db.data["users"][user.id] = user.to_dict()
    db.save()
    print("✅ User created with ID:", user.id)


# -------------------- TASK MANAGEMENT --------------------

class Task:
    def __init__(self, user_id, title, priority):
        self.id = generate_id()
        self.user_id = user_id
        self.title = title
        self.priority = priority
        self.status = "pending"
        self.created_at = current_time()
        self.completed_at = None

    def complete(self):
        self.status = "completed"
        self.completed_at = current_time()

    def to_dict(self):
        return self.__dict__


def add_task():
    user_id = input("Enter user ID: ")
    if user_id not in db.data["users"]:
        print("❌ User not found")
        return

    title = input("Task title: ")
    priority = input("Priority (low / medium / high): ").lower()

    task = Task(user_id, title, priority)
    db.data["tasks"][task.id] = task.to_dict()
    db.save()
    print("📌 Task added:", task.id)


def complete_task():
    task_id = input("Enter task ID: ")
    task = db.data["tasks"].get(task_id)

    if not task:
        print("❌ Task not found")
        return

    task["status"] = "completed"
    task["completed_at"] = current_time()
    db.save()
    print("✅ finished bro!!")


# -------------------- ANALYTICS --------------------

def productivity_report():
    report = defaultdict(int)

    for task in db.data["tasks"].values():
        report[task["status"]] += 1

    print("\n📊 Productivity Report")
    for status, count in report.items():
        print(f"{status.upper():<10}: {count}")


def user_task_summary():
    summary = defaultdict(int)

    for task in db.data["tasks"].values():
        summary[task["user_id"]] += 1

    print("\n👥 User Task Summary")
    for user_id, count in summary.items():
        user = db.data["users"].get(user_id)
        if user:
            print(f"{user['name']} → {count} tasks")


# -------------------- SIMULATION --------------------

def simulate_activity(n=20):
    if not db.data["users"]:
        print("⚠️ Create users first")
        return

    user_ids = list(db.data["users"].keys())
    priorities = ["low", "medium", "high"]

    for _ in range(n):
        user_id = random.choice(user_ids)
        task = Task(
            user_id,
            title=f"Auto Task {random.randint(100,999)}",
            priority=random.choice(priorities)
        )
        if random.choice([True, False]):
            task.complete()

        db.data["tasks"][task.id] = task.to_dict()

    db.save()
    print(f"🤖 Simulated {n} random tasks")


# -------------------- MENU --------------------

def menu():
    while True:
        print("""
========= PRODUCTIVITY SYSTEM =========
1. Create User
2. Add Task
3. Complete Task
4. Productivity Report
5. User Task Summary
6. Simulate Random Activity
7. Reset Database
0. Exit
""")
        choice = input("Choose option: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            add_task()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            productivity_report()
        elif choice == "5":
            user_task_summary()
        elif choice == "6":
            simulate_activity()
        elif choice == "7":
            db.reset()
            print("🗑 Database reset")
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


# -------------------- ENTRY POINT --------------------

if __name__ == "__main__":
    clear_screen()
    print("🚀 Welcome to the Productivity System")
    menu()
