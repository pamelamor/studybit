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

    if 'user_id' in session:

        return redirect('/workspace')
    
    elif 'user_id' not in session:

        return render_template('signin.html')
    

@app.route('/signup')
def signup():
    """View sign-up page."""

    return render_template('signup.html')
    
###################################################### WORKSPACE ROUTES
@app.route('/workspace')
def login():
    """Login to an existing account."""

    if 'user_id' in session:

        user = crud.get_user_by_id(session['user_id'])
        name = user.fname
        decks = crud.get_decks_by_user(user.user_id)

        return render_template('workspace.html', name=name, decks=decks)
    
    elif 'user_id' not in session:

        email = request.args.get("email")
        password = request.args.get("password")
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

            return render_template('workspace.html', name=name, decks=decks)


@app.route('/new-workspace', methods=["POST"])
def create_account():
    """Login to newly created account."""

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
    

@app.route('/delete-deck/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    """Remove deck from workspace through an AJAX request."""

    crud.remove_deck_by_id(deck_id)

    if crud.get_deck_by_id(deck_id) == None:

        msg = 'Successful deletion!'

        return msg
        
    elif crud.get_deck_by_id(deck_id) != None:

        msg = 'ERROR: Unsuccessful deletion.'

        return msg


###################################################### DESIGN SPACE ROUTES
@app.route('/create-deck')
def create_deck():
    """View design space for a new deck with no cards."""

    return render_template('create-deck.html')
    

@app.route('/customizer/<deck_id>')
def customizer(deck_id):
    """View design space for deck and its cards."""

    deck = crud.get_deck_by_id(deck_id)
    print(deck)
    flashcards = crud.get_flashcards_by_deck(deck_id)
    print(flashcards)

    return render_template('customizer.html', flashcards=flashcards, deck=deck)


@app.route("/delete-flashcard/<flashcard_id>", methods=['DELETE'])
def delete_flashcard(flashcard_id):
    """Remove flashcard from deck through an AJAX request."""

    crud.remove_flashcard_by_id(flashcard_id)

    if crud.get_flashcard_by_id(flashcard_id) == None:

        msg = 'Successful deletion!'

        return msg
        
    elif crud.get_flashcard_by_id(flashcard_id) != None:

        msg = 'ERROR: Unsuccessful deletion.'

        return msg


@app.route('/update-deck/<deck_id>', methods=['PUT'])
def deck_update(deck_id):
    """Update deck informarion."""

    deck = crud.get_deck_by_id(deck_id)
    deck.deck_name = request.form.get("deck_name")

    return redirect(f'/customizer/{deck_id}')




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)