import os



from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    users = db.execute("SELECT username, fullname, emailid FROM user_tbl").fetchall()
    for user in users:
        print(f"Username: {user.username} Full name: {user.fullname}, Email id:{user.emailid} ")

if __name__ == "__main__":
    main()