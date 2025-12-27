import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Pobiera URL bazy z systemu (z Docker Compose), a jeśli go nie ma, używa domyślnego
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost:5432/db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40))
    language = db.Column(db.String(40))

    def __init__(self,username,language):
        self.username = username
        self.language = language

# Ścieżki
@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/')
def index():
    all_users = User.query.all()
    return render_template('index.html', users=all_users), 200

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        username=request.form['username']
        language=request.form['language']
    if(username):
        user = User(username,language)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Baza danych została zainicjalizowana!")
    app.run(host="0.0.0.0",port=5000)
