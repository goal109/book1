import os

from flask import Flask,render_template,request,session,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    users = db.execute("SELECT * FROM user_tbl").fetchall()
    return render_template("index.html", users=users)

@app.route("/register", methods=["POST"])
def register():
    """Register user"""

    # Get form information.
    #name = request.form.get("name")
    uname=request.form.get("uname")
    upassword=request.form.get("upassword")
    fname=request.form.get("fname")
    ename=request.form.get("ename")


    # Make sure the username & email does not exist

    if db.execute("SELECT * FROM user_tbl WHERE username=:uname",{"uname":uname}).rowcount==1:
        return render_template("index.html",message="Username already exists")
    if db.execute("SELECT * FROM user_tbl WHERE emailid=:ename",{"ename":ename}).rowcount==1:
        return render_template("index.html", message="Email already exists")

    db.execute("INSERT INTO user_tbl (username,password,fullname,emailid) VALUES (:uname, :upassword,:fname,:ename)",
            {"uname":uname, "upassword":upassword,"fname":fname,"ename":ename})


    db.commit()
    return render_template("success.html")


@app.route("/login", methods=["GET","POST"])
def login():
    """Login user"""
    if request.method=="GET":
       return render_template("index.html")
    else:
    # Get form information.
    #name = request.form.get("name")
      uname=request.form.get("uname")
      upassword=request.form.get("upassword")


    # Make sure the username & email does not exist

    if db.execute("SELECT * FROM user_tbl WHERE username=:uname",{"uname":uname}).rowcount==0:
        return render_template("index.html", message1="Username does not exist")
    if db.execute("SELECT * FROM user_tbl WHERE password=:upassword",{"upassword":upassword}).rowcount==0:
        return render_template("index.html", message1="Wrong password")


    user_id = db.execute("SELECT id FROM user_tbl where username=:uname",{"uname":uname}).rowcount==1
    session["user_id"] = user_id
    return render_template("success.html")





    db.commit()

@app.route("/search",methods=["POST"])
def search():
    """LIst all books"""
    books=db.execute("SELECT * FROM book_tbl").fetchall()
    #books=db.execute("SELECT * FROM book_tbl ORDER BY year ASC").fetchall()

    return render_template("success.html",books=books)

@app.route("/search/<book_isbn>")
def book(book_isbn):
    """Lists details about a single book."""
    # Make sure flight exists.
    book = db.execute("SELECT * FROM book_tbl WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()
    if book is None:
       return render_template("error.html", message="No such book.")

         # Get all books.
    books = db.execute("SELECT title FROM book_tbl WHERE isbn= :book_isbn",
                                 {"book_isbn":book_isbn}).fetchall()
    return render_template("book.html", book=book, books=books)



@app.route("/users",methods=["POST"])
def users():
    """Lists all users."""
    users= db.execute("SELECT * FROM user_tbl").fetchall()
    return render_template("users.html",users=users)
