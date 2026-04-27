from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path using the NFS fix
DATABASE = 'file:/nfs/demo.db?vfs=unix-dotfile'

def get_db():
    db = sqlite3.connect(DATABASE, uri=True)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = 'OK'
        # SECURITY FEATURE: Added .strip() to sanitize inputs
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            if contact_id:
                db = get_db()
                db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
                db.commit()
                message = 'Contact deleted successfully.'
            return redirect(url_for('index', message=message))

        # SECURITY FEATURE: Added .strip() to sanitize inputs
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        if name and phone:
            db = get_db()
            db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            db.commit()
            message = 'Contact added successfully.'
        else:
            message = 'Missing name or phone number.'
        return redirect(url_for('index', message=message))

    message = request.args.get('message', '')
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Contacts</title></head>
        <body>
            <h2>Hitesh's Persistent & Secured Rolodex</h2>
            <form method="POST" action="{{ url_for('index') }}">
                <label>Name:</label><br><input type="text" name="name" required><br>
                <label>Phone:</label><br><input type="text" name="phone" required><br><br>
                <input type="submit" value="Submit">
            </form>
            {% if message %}<p>{{ message }}</p>{% endif %}
            {% if contacts %}
                <table border="1">
                    <tr><th>Name</th><th>Phone</th><th>Delete</th></tr>
                    {% for contact in contacts %}
                    <tr>
                        <td>{{ contact['name'] }}</td>
                        <td>{{ contact['phone'] }}</td>
                        <td>
                            <form method="POST">
                                <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                <input type="hidden" name="action" value="delete">
                                <input type="submit" value="Delete">
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}<p>No contacts found.</p>{% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
