'use strict';


//Delete deck from user workspace
const deckdeleteButtons = document.querySelectorAll('button.deckdeleteButton');

for (const deckdeleteButton of deckdeleteButtons) {
    deckdeleteButton.addEventListener('click', (evt) => {

        const deck_id = evt.target.id;
        const url = `/delete-deck/${deck_id}`;

        fetch(url, {
            method: 'DELETE',
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.text())
            .then((responseData) => {
                if(responseData == 'Successful deletion!'){
                    window.location.reload();
                }
                else{
                    console.log(responseData);
                }
            });
    });
};


//Delete flashcard from user deck and design space
const flashdeleteButtons = document.querySelectorAll('button.flashdeleteButton');

for (const flashdeleteButton of flashdeleteButtons) {
    flashdeleteButton.addEventListener('click', (evt) => {
        const flashcard_id = evt.target.id;
        const url = `/delete-flashcard/${flashcard_id}`;

        fetch(url, {
            method: 'DELETE',
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.text())
            .then((responseData) => {
                if(responseData == 'Successful deletion!'){
                    window.location.reload();
                }
                else{
                    console.log(responseData);
                }
            });
    });
};

  
    
