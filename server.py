"""Server for flashcard app."""

from flask import (Flask, render_template, request, session, redirect, flash)
import jinja2
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    print(session)
    session.clear()
    print(session)
    return render_template('homepage.html')

@app.route('/signup')
def signup():
    """View sign-up page."""

    print(session)
    return render_template('signup.html')


@app.route('/new-workspace', methods=["POST"])
def create_account():
    """Create a new account."""

    #We have to take care of the instance where email and password are not entered by the user
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    if(crud.get_user_by_email(email) == None):
        flash("Successful Creation!")
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.user_id
        session['email'] = user.email
        name = user.fname
        return render_template('workspace.html', name=name)
    elif(crud.get_user_by_email(email) != None ):
        flash("This email is already registered.") 
        return redirect('/signup')


@app.route('/signin')
def signin():
    """View sign-in page."""
    
    print(session)
    return render_template('signin.html')


@app.route('/workspace', methods=["POST"])
def login():
    """Login existing to an existing account."""

    #We have to take care of the instance where email and password are not entered by the user
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if(user == None or user.password != password ):
        flash("Wrong information. Try again") 
        return redirect('/signin')
    elif(user != None and user.password == password):
        flash("Success Log in!")
        session['user_id'] = user.user_id
        session['email'] = user.email
        decks = crud.get_decks_by_user(user.user_id)
        name = user.fname
        print(session)
        return render_template('workspace.html', name=name, decks=decks)




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)