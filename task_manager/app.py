import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id} {self.title}>'


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description')
    due_date = StringField('Due date (YYYY-MM-DD)')
    completed = BooleanField('Completed')
    submit = SubmitField('Save')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


# Ensure tables exist (call directly for compatibility)
with app.app_context():
    db.create_all()
    # Seed sample tasks if DB is empty
    if Task.query.count() == 0:
        sample = [
            Task(title='Buy groceries', description='Milk, eggs, bread', due_date=(datetime.utcnow().date()).isoformat()),
            Task(title='Read book', description='Finish chapter 4', due_date=''),
            Task(title='Call Alice', description='Discuss project', due_date='')
        ]
        db.session.add_all(sample)
        db.session.commit()


@app.route('/')
def index():
    status = request.args.get('status', 'all')
    q = request.args.get('q', '').strip()
    tasks = Task.query
    if status == 'completed':
        tasks = tasks.filter_by(completed=True)
    elif status == 'pending':
        tasks = tasks.filter_by(completed=False)
    if q:
        tasks = tasks.filter(Task.title.contains(q))
    tasks = tasks.order_by(Task.created_at.desc()).all()
    delete_form = DeleteForm()
    return render_template('index.html', tasks=tasks, status=status, q=q, delete_form=delete_form)


@app.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        # validate due date format (optional)
        due_raw = (form.due_date.data or '').strip()
        if due_raw:
            try:
                datetime.strptime(due_raw, '%Y-%m-%d')
            except ValueError:
                flash('Due date must be YYYY-MM-DD')
                return render_template('add_task.html', form=form)

        t = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=due_raw,
            completed=form.completed.data,
        )
        db.session.add(t)
        db.session.commit()
        flash('Task added.')
        return redirect(url_for('index'))
    return render_template('add_task.html', form=form)


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        # validate due date format (optional)
        due_raw = (form.due_date.data or '').strip()
        if due_raw:
            try:
                datetime.strptime(due_raw, '%Y-%m-%d')
            except ValueError:
                flash('Due date must be YYYY-MM-DD')
                return render_template('edit_task.html', form=form, task=task)

        task.title = form.title.data
        task.description = form.description.data
        task.due_date = due_raw
        task.completed = form.completed.data
        db.session.commit()
        flash('Task updated.')
        return redirect(url_for('index'))
    return render_template('edit_task.html', form=form, task=task)


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
