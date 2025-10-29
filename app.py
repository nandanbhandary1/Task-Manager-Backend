# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from models import db, Task, SubTask

# app = Flask(__name__)
# CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
# db.init_app(app)

# with app.app_context():
#     db.create_all()


# # Add new task
# @app.route("/tasks", methods=["POST"])
# def add_task():
#     data = request.json
#     new_task = Task(title=data["title"], description=data["description"])
#     db.session.add(new_task)
#     db.session.commit()
#     return jsonify({"message": "Task created successfully!"})


# # Get all tasks
# @app.route("/tasks", methods=["GET"])
# def get_tasks():
#     tasks = Task.query.all()
#     task_list = []
#     for task in tasks:
#         task_list.append(
#             {
#                 "id": task.id,
#                 "title": task.title,
#                 "description": task.description,
#                 "completed": task.completed,
#                 "subtasks": [
#                     {
#                         "id": sub.id,
#                         "detail": sub.detail,
#                         "time_required": sub.time_required,
#                         "done": sub.done,
#                     }
#                     for sub in task.subtasks
#                 ],
#             }
#         )
#     return jsonify(task_list)


# # Add subtask
# @app.route("/tasks/<int:task_id>/subtasks", methods=["POST"])
# def add_subtask(task_id):
#     data = request.json
#     sub = SubTask(
#         task_id=task_id,
#         detail=data["detail"],
#         time_required=data.get("time_required", ""),
#         done=False,
#     )
#     db.session.add(sub)
#     db.session.commit()
#     return jsonify({"message": "Subtask added successfully!"})


# # Toggle subtask completion
# @app.route("/subtasks/<int:subtask_id>", methods=["PATCH"])
# def toggle_subtask(subtask_id):
#     sub = SubTask.query.get(subtask_id)
#     sub.done = not sub.done
#     db.session.commit()


# # Mark entire task complete manually (user-controlled)
# @app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
# def complete_task(task_id):
#     task = Task.query.get(task_id)
#     if not task:
#         return jsonify({'error': 'Task not found'}), 404

#     task.completed = True
#     db.session.commit()
#     return jsonify({'message': 'Task marked as complete manually!'})


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Task, SubTask

app = Flask(__name__)
CORS(app)

# Configure SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = Task(title=data["title"], description=data["description"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully!"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "subtasks": [
                    {
                        "id": sub.id,
                        "detail": sub.detail,
                        "time_required": sub.time_required,
                        "done": sub.done,
                    }
                    for sub in task.subtasks
                ],
            }
        )
    return jsonify(task_list)


@app.route("/tasks/<int:task_id>/subtasks", methods=["POST"])
def add_subtask(task_id):
    data = request.json
    sub = SubTask(
        task_id=task_id,
        detail=data["detail"],
        time_required=data.get("time_required", ""),
        done=False,
    )
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Subtask added successfully!"})


@app.route("/subtasks/<int:subtask_id>", methods=["PATCH"])
def toggle_subtask(subtask_id):
    sub = SubTask.query.get(subtask_id)
    if not sub:
        return jsonify({"error": "Subtask not found"}), 404

    sub.done = not sub.done
    db.session.commit()
    return jsonify({"message": "Subtask updated successfully!"})


@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not task.completed:
        task.completed = True
        db.session.commit()

    return jsonify({"message": "Task marked as complete manually!"})


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Delete all subtasks first
    for sub in task.subtasks:
        db.session.delete(sub)

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})


if __name__ == "__main__":
    app.run(debug=True)
