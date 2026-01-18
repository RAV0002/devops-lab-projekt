import sys
import csv
import json
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
        os.makedirs('seed/output', exist_ok=True)

        # CSV
        with open('seed/output/users.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["username","language"])
            writer.writeheader()
            for user in users:
                writer.writerow({'username':user.username, 'language':user.language})

        #JSON
        with open('seed/output/data.json','w') as file:
            json_data_list = [{"username":user.username, "language":user.language} for user in users]
            json.dump(json_data_list,file,indent=4)

        # LOG
        with open('seed/output/seed.log','w') as file:
            file.write("Seeder added 5 users.\n")
        
        print("Seeding is completed!")

if __name__ == '__main__':
    seed_data()