import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    body = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id} {self.title}>'


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=100)])
    body = TextAreaField('Body')
    submit = SubmitField('Save')


def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/')
def index():
    q = request.args.get('q', '').strip()
    notes = Note.query.order_by(Note.updated_at.desc())
    if q:
        search = f'%{q}%'
        notes = notes.filter(
            db.or_(
                Note.title.ilike(search),
                Note.body.ilike(search),
                Note.tags.ilike(search),
            )
        )
    notes = notes.all()
    return render_template('index.html', notes=notes, q=q)


@app.route('/note/<int:note_id>')
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            tags=form.tags.data,
            body=form.body.data,
        )
        db.session.add(note)
        db.session.commit()
        flash('Note created successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_note.html', form=form, action='Add Note')


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.tags = form.tags.data
        note.body = form.body.data
        db.session.commit()
        flash('Note updated successfully.', 'success')
        return redirect(url_for('view_note', note_id=note.id))
    return render_template('edit_note.html', form=form, action='Edit Note')


@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'warning')
    return redirect(url_for('index'))


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
