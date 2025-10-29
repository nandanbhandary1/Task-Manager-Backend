from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    subtasks = db.relationship("SubTask", backref="task", cascade="all, delete")


class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    detail = db.Column(db.String(255), nullable=False)
    time_required = db.Column(db.String(50))
    done = db.Column(db.Boolean, default=False)
