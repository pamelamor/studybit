"""Model for language study flashcard app."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    decks = db.relationship("Deck", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname} lname={self.lname}>"


class Deck(db.Model):
    """A deck."""

    __tablename__ = "decks"

    deck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    deck_name = db.Column(db.String, nullable = False)
    # deck_color = db.Column(db.String, nullable = False)
    # deck_font = db.Column(db.String, nullable = False)
    # deck_font_color = db.Column(db.String, nullable = False)
    # deck_img = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)

    user = db.relationship("User", back_populates="decks")
    flashcards = db.relationship("Flashcard", back_populates="deck")
   
    def __repr__(self):
        return f"<Deck deck_id={self.deck_id} user_id={self.user_id} deck_name={self.deck_name}>"
    

class Flashcard(db.Model):
    """A flashcard."""

    __tablename__ = "flashcards"

    flashcard_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    front_content = db.Column(db.String, nullable = False)
    back_content = db.Column(db.String, nullable = False)
    # flashcard_img = db.Column(db.String, nullable = False)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.deck_id"), nullable = False)

    deck = db.relationship("Deck", back_populates="flashcards")
   
    def __repr__(self):
        return f"<Flashcard flashcard_id={self.flashcard_id} deck_id={self.deck_id}>"
    

######################################################################################
def connect_to_db(flask_app, db_uri="postgresql:///cap_app", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)