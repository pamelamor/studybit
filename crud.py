"""CRUD operations = Create, Read, Update, Delete operations"""

from model import User, Deck, Flashcard, connect_to_db, db


def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

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
    User.query.filter(User.user_id == user_id).delete()
    db.session.commit()


################################################################################################################################################
def create_deck(name, user_id):
    """Create and return a new deck."""

    deck = Deck(deck_name=name, user_id=user_id)

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
    Deck.query.filter(Deck.deck_id == deck_id).delete()
    db.session.commit()


def remove_decks_by_user(user_id):
    """Remove decks by user.""" 

    decks = Deck.query.filter(Deck.user_id == user_id).all()
    for deck in decks:
        remove_deck_by_id(deck.deck_id)
    db.session.commit()


################################################################################################################################################
def create_flashcard(deck_id, front, back):
    """Create and return a new flashcards"""

    flashcard = Flashcard(deck_id=deck_id, front_content=front, back_content=back)

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

    Flashcard.query.filter(Flashcard.flashcard_id == flashcard_id).delete()
    db.session.commit()


def remove_flashcards_by_deck(deck_id):
    """Remove flashcards by deck.""" 

    Flashcard.query.filter(Flashcard.deck_id == deck_id).delete()
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)