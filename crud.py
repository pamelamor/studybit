"""CRUD operations = Create, Read/Get, Update, Delete operations"""

from model import User, Deck, Flashcard, connect_to_db, db


def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return user by ID."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return user by email."""

    return User.query.filter(User.email == email).first()


def remove_user_by_id(user_id):
    """Remove user."""

    remove_decks_by_user(user_id)
    db.session.delete(get_user_by_id(user_id))
    db.session.commit()


################################################################################################################################################
def create_deck(name, user_id, img_url=None):
    """Create and return a new deck."""

    deck = Deck(deck_name=name, user_id=user_id, deck_img_url=img_url)
    db.session.add(deck)
    db.session.commit()

    return deck


def get_all_decks():
    """Return all decks."""

    return Deck.query.all()


def get_deck_by_id(deck_id):
    """Return deck by ID."""

    return Deck.query.get(deck_id)


def get_decks_by_user(user_id):
    """Return decks by user."""

    return Deck.query.filter(Deck.user_id == user_id).all()


def remove_deck_by_id(deck_id):
    """Remove deck by ID.""" 

    remove_flashcards_by_deck(deck_id)
    db.session.delete(get_deck_by_id(deck_id))
    db.session.commit()


def remove_decks_by_user(user_id):
    """Remove decks by user.""" 

    decks = get_decks_by_user(user_id)
    for deck in decks:
        remove_deck_by_id(deck.deck_id)
    db.session.commit()


#The img, font, deck_color and font_color properties haven't been included for updates yet 
# (must be optional when implemented), only deck_name is required for an update request to the DB
def update_deck_by_id(deck_id, deck_name, deck_img):
    """Update deck information by id""" 

    Deck.query.filter(Deck.deck_id == deck_id).update({"deck_name": deck_name,
                                                       "deck_img_url": deck_img})
    db.session.commit()


################################################################################################################################################
def create_flashcard(deck_id, front, back):
    """Create and return a new flashcards"""

    flashcard = Flashcard(deck_id=deck_id, front_content=front, back_content=back)
    db.session.add(flashcard)
    db.session.commit()

    return flashcard


def get_all_flashcards():
    """Return all flashcards."""

    return Flashcard.query.all()


def get_flashcard_by_id(flashcard_id):
    """Return flashcard by id."""

    return Flashcard.query.get(flashcard_id)


def get_flashcards_by_deck(deck_id):
    """Return flashcards by deck."""

    return Flashcard.query.filter(Flashcard.deck_id == deck_id).all()


def remove_flashcard_by_id(flashcard_id):
    """Remove flashcard by id""" 

    db.session.delete(get_flashcard_by_id(flashcard_id))
    db.session.commit()


def remove_flashcards_by_deck(deck_id):
    """Remove flashcards by deck.""" 

    flashcards = get_flashcards_by_deck(deck_id)
    for flashcard in flashcards:
        remove_flashcard_by_id(flashcard.flashcard_id)
    db.session.commit()


#The img property hasn't been included for updates yet (must be optional when implemented), 
# only front_content and back_content are required for an update request to the DB
def update_flashcard_by_id(flashcard_id, front_content, back_content):
    """Update flashcard information by id""" 

    Flashcard.query.filter(Flashcard.flashcard_id == flashcard_id).update({"front_content": front_content,
                                                                           "back_content": back_content })
    db.session.commit()

    

######################################################################################
if __name__ == '__main__':
    from server import app
    connect_to_db(app)