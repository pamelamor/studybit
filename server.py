"""Server for flashcard app."""

from flask import (Flask, render_template, request, session, redirect, flash, jsonify)
import jinja2
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

###################################################### SIGNIN/UP ROUTES
@app.route('/')
def homepage():
    """View homepage."""

    session.clear()

    return render_template('homepage.html')

@app.route('/signin')
def signin():
    """View sign-in page."""

    return render_template('signin.html')
    
#BLOCK#1: Prevent a user from loading the login page if they are logged in.
# @app.route('/signin')
# def signin():
#     """View sign-in page."""
#
#     if 'user_id' in session:
#         return redirect('/workspace')
#     elif 'user_id' not in session:
#         return render_template('signin.html')
    

@app.route('/signup')
def signup():
    """View sign-up page."""

    return render_template('signup.html')
    

@app.route('/login-signup', methods=['GET','POST'])
def login_signup():
    """Login to an existing account or signup."""

    #BLOCK#1: Prevent a user from loading the login page if they are logged in.
    # if 'user_id' in session:
    #     user = crud.get_user_by_id(session['user_id'])
    #     name = user.fname
    #     decks = crud.get_decks_by_user(user.user_id)
    #     return render_template('workspace.html', name=name, decks=decks)
    # elif 'user_id' not in session:

    if request.method == 'GET':

        email = request.args.get("email")
        password = request.args.get("password")
        user = crud.get_user_by_email(email)
            
        if(user == None or user.password != password ):

            flash("Wrong information. Try again") 

            return redirect('/signin')
            
        elif(user != None and user.password == password):

            session['user_id'] = user.user_id
            session['email'] = user.email
            decks = user.decks
            name = user.fname

            return render_template('workspace.html', name=name, decks=decks)
        
    elif request.method == 'POST':

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")
        user = crud.get_user_by_email(email)

        if(user == None):

            flash("You may now login.")
            user = crud.create_user(fname, lname, email, password)

            return redirect('/signin')
    
        elif(user != None ):

            flash("This email is already registered.") 

            return redirect('/signup')
    

###################################################### WORKSPACE ROUTES
@app.route('/workspace')
def workspace():
    """View workspace page."""
     
    user = crud.get_user_by_id(session['user_id'])
    name = user.fname
    decks = user.decks

    return render_template('workspace.html', name=name, decks=decks)


#BLOCK#2: Create a deck asynchrounously with AJAX.
# @app.route('/create-deck')
# def create_deck():
#     """Create deck in workspace through an AJAX requests."""

#     deck = crud.create_deck("untitled", session['user_id'])
#     return {"deck_name": deck.deck_name, "deck_id": deck.deck_id}


@app.route('/create-deck')
def create_deck():
    """Create deck in workspace."""

    crud.create_deck("untitled", session['user_id'])
    
    return redirect('/workspace')


@app.route('/delete-deck/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    """Remove deck from workspace through an AJAX request."""

    crud.remove_deck_by_id(deck_id)

    if crud.get_deck_by_id(deck_id) == None:

        return 'Successful deletion!'
    
    elif crud.get_deck_by_id(deck_id) != None:

        return 'ERROR: Unsuccessful deletion.'


###################################################### DESIGN SPACE ROUTES
@app.route('/create-flashcard/<deck_id>', methods=['POST'])
def create_flashcard(deck_id):
    """Create flashcard for deck through an AJAX requests."""

    front = request.form.get('front')
    back = request.form.get('back')
    # crud.create_flashcard(deck_id, front, back)

    return 'success!'


@app.route("/delete-flashcard/<flashcard_id>", methods=['DELETE'])
def delete_flashcard(flashcard_id):
    """Remove flashcard from deck through an AJAX request."""

    crud.remove_flashcard_by_id(flashcard_id)

    if crud.get_flashcard_by_id(flashcard_id) == None:

        return 'Successful deletion!'
        
    elif crud.get_flashcard_by_id(flashcard_id) != None:

        return 'ERROR: Unsuccessful deletion.'


@app.route('/edit-deck/<deck_id>', methods=['GET','POST'])
def edit_deck(deck_id):
    """View/Edit deck in design space."""

    if request.method == 'GET':
        deck = crud.get_deck_by_id(deck_id)
        flashcards = crud.get_flashcards_by_deck(deck_id)

        return render_template('customizer.html', flashcards=flashcards, deck=deck)
    
    # # You can turn this into an AJAX POST request that way the reload doesnt happen
    # elif request.method == 'POST':

    #     deck_name = request.form.get('deck_name')
    #     crud.update_deck_by_id(deck_id, deck_name)
        

    #     return redirect(f'/edit-deck/{deck_id}')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)