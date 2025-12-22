from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@localhost/users'

db=SQLAlchemy(app)

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
    return render_template('index.html', users=all_users)

@app.route('/submit',methods=['POST'])
def submit():
    if request.method == 'POST':
        username=request.form['username']
        language=request.form['language']
    user = User(username,language)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)