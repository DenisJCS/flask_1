from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'jach_london'
notes = []
@app.route('/')
def home():
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
        
        # Add this note to our list
        note = {
            'id': len(notes) + 1,
            'title': title,
            'content': content,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        notes.append(note)

        flash('Note added successfuly!')
        return redirect(url_for('home'))
    # If it's a GET request, just show the form
    return render_template('add_note.html')

@app.route('/note/<int:note_id>')
def view_note(note_id):
    """Find the note with the given ID"""
    note = next((note for note in notes if note['id'] == note_id), None)

    if note is None:
        flash('Note not found!')
        return redirect(url_for('home'))
    
    return render_template('view_note.html', note=note)


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
    app.run(debug=True)

