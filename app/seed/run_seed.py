import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app, db, User

def seed_data():
    users = [
        User(username='Krzysztof', language='Polish'),
        User(username='Damon', language='English'),
        User(username='Juan', language='Spanish'),
        User(username='Kendrick', language='English'),
        User(username='Kuba', language='Polish')
    ]

    with app.app_context():
        db.create_all()

        for user in users:
            exist = User.query.filter_by(username=user.username).first()
            if not exist:
                db.session.add(user)
                print(f"Added user: {user.username}")
        db.session.commit()
        print("Data base has been filled")

if __name__ == '__main__':
    seed_data()