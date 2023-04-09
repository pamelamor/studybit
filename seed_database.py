"""Script to seed database."""

import os

import crud
import model
import server

os.system('dropdb cap_app')
os.system('createdb cap_app')

model.connect_to_db(server.app)
model.db.create_all()

# Create users
users = []

user1 = crud.create_user("Pamela", "Ortiz", "pamela@gmail.com", "pp")
user2 = crud.create_user("Leo", "Ortiz", "leo@gmail.com", "lp")
user3 = crud.create_user("Massiel", "Ortiz", "massiel@gmail.com", "mp")

users.append(user1)
users.append(user2)
users.append(user3)

model.db.session.add_all(users)
model.db.session.commit()


#Create decks 
decks = []

deck1 = crud.create_deck("Japanese", user1.user_id)
deck2 = crud.create_deck("Spanish", user2.user_id)
deck3 = crud.create_deck("English", user3.user_id)
deck4 = crud.create_deck("Portuguese", user1.user_id)

decks.append(deck1)
decks.append(deck2)
decks.append(deck3)
decks.append(deck4)

model.db.session.add_all(decks)
model.db.session.commit()


# Create flashcards 
flashcards = []

flashcard1 = crud.create_flashcard(deck1.deck_id, "ありがとう", "Thank you (informal)")
flashcard2 = crud.create_flashcard(deck1.deck_id, "さようなら", "Goodbye")
flashcard3 = crud.create_flashcard(deck1.deck_id, "おはよう", "Hello/Good morning (informal)")

flashcard4 = crud.create_flashcard(deck2.deck_id, "Gracias", "Thank you")
flashcard5 = crud.create_flashcard(deck2.deck_id, "Adios", "Goodbye")
flashcard6 = crud.create_flashcard(deck2.deck_id, "Hola", "Hello")

flashcard7 = crud.create_flashcard(deck3.deck_id, "Thank you", "Gracias")
flashcard8 = crud.create_flashcard(deck3.deck_id, "Goodbye", "Adios")
flashcard9 = crud.create_flashcard(deck3.deck_id, "Hello", "Hola")

flashcard10 = crud.create_flashcard(deck4.deck_id, "Obrigada", "Gracias")
flashcard11 = crud.create_flashcard(deck4.deck_id, "Adeus", "Adios")
flashcard12 = crud.create_flashcard(deck4.deck_id, "Olá", "Hola")

flashcards.append(flashcard1)
flashcards.append(flashcard2)
flashcards.append(flashcard3)
flashcards.append(flashcard4)
flashcards.append(flashcard5)
flashcards.append(flashcard6)
flashcards.append(flashcard7)
flashcards.append(flashcard8)
flashcards.append(flashcard9)
flashcards.append(flashcard10)
flashcards.append(flashcard11)
flashcards.append(flashcard12)

model.db.session.add_all(flashcards)
model.db.session.commit()

