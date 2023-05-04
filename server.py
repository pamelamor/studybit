"""Server for flashcard app."""

from flask import (Flask, render_template, request, session, redirect, flash, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud
import os
import requests
import cloudinary.uploader


CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUDINARY_NAME = 'darjy6jqz'

GOOGLE_FONTS_KEY = os.environ['GOOGLE_FONTS_KEY']
GOOGLE_FONTS_KEY = os.environ['GOOGLE_FONTS_KEY']


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
        phone_num = request.form.get("phone_number")
        password = request.form.get("password")
        user = crud.get_user_by_email(email)

        if(user == None):

            flash("You may now login.")
            user = crud.create_user(fname, lname, email, password, phone_num)

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

        deck_font_color = request.form.get('deck_font_color')
        deck_font = request.form.get('deck_font')
        deck_color = request.form.get('deck_color')
        crud.update_deck_by_id(deck_id,deck_name,deck_img_url, deck_font, deck_font_color, deck_color)

        return jsonify({'deck_name': deck_name, "deck_img_url": deck_img_url, "deck_font": deck_font, 
                        "deck_font_color": deck_font_color, "deck_color": deck_color, "msg": "Deck information updated."})


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

    front = request.form.get('front_content')
    back = request.form.get('back_content')
    img_file = request.files['flashcard_img']


    if img_file.filename == "dummyfile.png":

        flashcard = crud.get_flashcard_by_id(flashcard_id)
        image = flashcard.flashcard_img

    else:
                
        result = cloudinary.uploader.upload(img_file, 
                                            api_key=CLOUDINARY_KEY,
                                            api_secret=CLOUDINARY_SECRET,
                                            cloud_name=CLOUDINARY_NAME)
        image = result['secure_url']


    crud.update_flashcard_by_id(flashcard_id, front, back, image)

    return {'front_content': front, 'back_content': back, 'flashcard_img': image, "msg": "Flashcard information updated."}


###################################################### STUDY SESSION ROUTES
@app.route('/study-session/<deck_id>', methods=['GET', 'POST'])
def study_session(deck_id):


    if request.method == 'GET':

        deck = crud.get_deck_by_id(deck_id)
        flashcards = crud.get_flashcards_by_deck(deck_id)

        if(flashcards == []):
            flash('This deck has does not have flashcards yet!')
            return redirect('/workspace')

        else:
            i = -1
            progress = -( i / len(flashcards)) * 100

            return render_template('studysession.html', deck=deck, flashcards=flashcards, i=i, progress=progress)
    
    elif request.method == 'POST':

        flashcards = crud.get_flashcards_by_deck(deck_id)
        
        i = int(request.json.get('i'))
        if i - 1 < -len(flashcards):
            progress = 100

            return jsonify({'msg': "Finished!", "progress": progress})
        else:
            i -= 1
            next_flashcard = flashcards[i]
            progress = -( i / len(flashcards)) * 100
            print('*********************')
            print(len(flashcards))

            return jsonify({'i': i , 'front': next_flashcard.front_content, 'back': next_flashcard.back_content, 'img': next_flashcard.flashcard_img, "progress": progress})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)