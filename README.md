# ![MasterHead](studibit.png)

# What is Studybit?
- Studybit is a flashcard app that aims to provide users with a free and intuitive way to create foreign study language materials! The web-app allows users to create an account that require a phone number at registration. With this information Studybit is able to send daily study reminders by utilizing the Twilio API and a crontab script that runs in the background. This app also gives users the power to personalize their materials in hopes of making learning more fun and flexible. Users can create, delete, modify and customize flashcards and decks in Design Space/ Workspace, and are able to see their styling come to life in study sessions where they can practice their languages.

## Project Tech Stack:
- Python | Flask | PostgreSQL | SQLAlchemy | JavaScript | AJAX | HTML/CSS | Bootstrap | Jinja | Crontab | Shell

## APIs used:
- [Cloudinary Upload API](https://cloudinary.com/documentation/image_upload_api_reference)
- [Google Fonts API](https://developers.google.com/fonts/docs/developer_api)
- [Twilio SMS API](https://www.twilio.com/docs/sms/api)

## Data Model:
![Data Model HW#5-2](https://user-images.githubusercontent.com/89920108/236864227-f16d11dc-0c99-453b-925d-534ce28c2e60.png)
[dbdiagram.io](https://dbdiagram.io/d/6429b5d45758ac5f17261779)

## Future Implementations
  - Unit/Integrated testing
  - Secure Log-in process
  - Light/Dark mode
  - Adding sound to cards
  - Study music playlist/player
  - Streak Tracker Calendar/Clock display
  - Pomodoro/Cutomizable timed study sessions w/ visual countdown
  - Progress report page that allows users to monitor their progress on a flashcard deck
  - Allow the user to pick how many cards, or which cards, from a deck they would like to study
  - Have a spacial repetition algorithm pick the cards you will review based on your progress reports.
  - Other flashcard games → Typing answers, Tile page flipping, reverse cards so we review from back to front
  - Community data/ ability to share set with friends and keep a score on who has the best streak of correct answers
