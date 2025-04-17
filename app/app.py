from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'jach_london'
notes = []

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Note model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    # Get all the notes from database
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return render_template('home.html', notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Simple validation
        if not title or not content:
            flash('Title and content are required!')
            return render_template('add_note.html')
        
        # Create a new note in the database
        new_note = Note(title=title, content=content)
        db.session.add(new_note)
        db.session.commit()

        flash('Note added successfully!')
        return redirect(url_for('home'))
    
    # If it's a GET request, just show the form 
    return render_template('add_note.html')

@app.route('/note/<int:note_id>')
def view_note(note_id):
    """Find the note with the given ID"""
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)

@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('This and content are required!')
            return render_template
        
        #Update the note
        note.title = title
        note.content = content
        db.session.commit()

        flash('Note updated successfuly!')
        return redirect(url_for('view_note', note_id=note.id))
    
    return render_template('edit_note.html', note=note)

@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note=Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()

    flash('Note deleted successfully!')
    return render_template(url_for('home'))


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name or 'World')

@app.route('/user/<username>')
def show_user(username):
    # URL variable captured as function paramater
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post: {post_id}'

@app.route('/form', methods= ['GET', 'POST'])
def form():
    name = None
    if request.metod == 'POST':
        name = request.form.get('name', '')
    return render_template('form.html', name=name)

# Run the application if this file is executed directly
if __name__ == '__main__':
    with app.context():
        db.create_all() # Create database tables
    app.run(debug=True)

