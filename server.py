"""Server for flashcard app."""

from flask import (Flask, render_template, request, session, redirect, flash, jsonify,json)
from jinja2 import StrictUndefined
from model import connect_to_db, db
from twilio.rest import Client
from datetime import datetime
import jinja2
import crud
import os
import requests
import random
import cloudinary.uploader
import urllib.request


CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUDINARY_NAME = 'darjy6jqz'

GOOGLE_FONTS_KEY = os.environ['GOOGLE_FONTS_KEY']
GOOGLE_FONTS_KEY = os.environ['GOOGLE_FONTS_KEY']

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
TWIILIO_NUM = os.environ['TWIILIO_NUM']
MY_NUM = os.environ['MY_NUM']


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

###################################################### TWILIO API
# client = Client(ACCOUNT_SID, AUTH_TOKEN)
# print(repr(datetime.utcnow()))

# message = client.messages \
#     .create(
#          messaging_service_sid = 'MG1226bd960a44a56fe787f2dc71c59d46',
#          body = 'It works!',
#          send_at = datetime(2023, 4, 25, 15, 00, 00),
#          schedule_type = 'fixed',
#          to = MY_NUM
#      )

# print(message.sid)

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
@app.route('/edit-deck/<deck_id>', methods=['GET','POST'])
def edit_deck(deck_id):
    """View/Edit deck in design space."""


    if request.method == 'GET':

        url = f'https://www.googleapis.com/webfonts/v1/webfonts?key={GOOGLE_FONTS_KEY}'
        result = requests.get(url)
        data = result.json()

        fonts = []
        for obj in data['items']:
            fonts.append(obj['family'])

        deck = crud.get_deck_by_id(deck_id)
        flashcards = crud.get_flashcards_by_deck(deck_id)
        session['deck_id'] = deck.deck_id    
    

        return render_template('customizer.html', flashcards=flashcards, deck=deck, fonts=fonts)
    

    #BLOCK#3: Allow for the user to send singular field data while leaving the rest empty.
    elif request.method == 'POST':

        deck_name = request.form.get('deck_name')
        img_file = request.files['deck_img']

        if img_file.filename == "dummyfile.png":

            deck = crud.get_deck_by_id(deck_id)
            deck_img_url = deck.deck_img_url

        else:
                
            result = cloudinary.uploader.upload(img_file, 
                                            api_key=CLOUDINARY_KEY,
                                            api_secret=CLOUDINARY_SECRET,
                                            cloud_name=CLOUDINARY_NAME)
            deck_img_url = result['secure_url']

        deck_font = request.form.get('deck_font')
        deck_font_color = request.form.get('deck_font_color')
        crud.update_deck_by_id(deck_id,deck_name,deck_img_url, deck_font, deck_font_color)

        return jsonify({'deck_name': deck_name, "deck_img_url": deck_img_url, "deck_font": deck_font, 
                        "deck_font_color": deck_font_color})
    

#BLOCK#2: Create a flashcard asynchrounously with AJAX.
# @app.route('/create-flashcard', methods=['POST'])
# def create_flashcard():
#     """Create flashcard for deck through an AJAX requests."""

#     front = request.json.get('front_content')
#     back = request.json.get('back_content')
#     flashcard = crud.create_flashcard(session['deck_id'], front, back)

#     return {'flashcard_id': flashcard.flashcard_id, 'front_content': flashcard.front_content}


@app.route('/create-flashcard', methods=['POST'])
def create_flashcard():
    """Create deck in design space."""

    front = request.form.get('front_content')
    back = request.form.get('back_content')
    crud.create_flashcard(session['deck_id'], front, back)

    return redirect(f'/edit-deck/{session["deck_id"]}')


@app.route("/delete-flashcard/<flashcard_id>", methods=['DELETE'])
def delete_flashcard(flashcard_id):
    """Remove flashcard from deck through an AJAX request."""

    crud.remove_flashcard_by_id(flashcard_id)

    if crud.get_flashcard_by_id(flashcard_id) == None:

        return 'Successful deletion!'
        
    elif crud.get_flashcard_by_id(flashcard_id) != None:

        return 'ERROR: Unsuccessful deletion.'
    

@app.route('/edit-flashcard/<flashcard_id>', methods=['POST'])
def edit_flashcard(flashcard_id):

    front = request.json.get('front_content')
    back = request.json.get('back_content')
    crud.update_flashcard_by_id(flashcard_id, front, back)

    return {'front_content': front}


###################################################### STUDY SESSION ROUTES
@app.route('/study-session/<deck_id>', methods=['GET', 'POST'])
def study_session(deck_id):


    if request.method == 'GET':

        deck = crud.get_deck_by_id(deck_id)
        flashcards = crud.get_flashcards_by_deck(deck_id)
        i = -1
        
        return render_template('studysession.html', deck=deck, flashcards=flashcards, i=i)
    
    elif request.method == 'POST':

        flashcards = crud.get_flashcards_by_deck(deck_id)
        
        i = int(request.json.get('i'))
        if i - 1 < -len(flashcards):

            return jsonify({'msg': "Finished!"})
        else:

            next_flashcard = flashcards[i-1]

            return jsonify({'i': i - 1, 'front': next_flashcard.front_content, 'back': next_flashcard.back_content})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)