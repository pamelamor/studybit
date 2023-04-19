'use strict';

//######################################################################### Deck requests
//BLOCK#2: Create a deck asynchrounously through AJAX without having to return HTLM code. Once
//implemented, this request hopefully also allows you to delete decks asynchrounously. So far, when you 
//create an async deck with the request below, it seems like "the way in which the deck is created"
//interferes with you deleting the new deck asynchrounously as well. What's supposed to be an async deletion 
//takes effect after you reload the page, which, if you think about it, defeats the purpose of AJAX. -------> I figured it out!

//The reason why the above happens is because when we create a new deck or flashcard, and try to delete it, the process of adding an
//eventListenier to the button never happens, this process only occurs when we navigate to /edit-deck/<deck_id>. We will try to solve this
//moving forward.

// const createDeck = document.getElementById('create-deck'); ---> try to make this POST request like we did for the flashcard
// if(createDeck){
//     createDeck.addEventListener('click', (evt) => {
//         evt.preventDefault()
//         fetch('/create-deck')
//             .then((response) => response.json())
//             .then((responseData) => {
//                 const decks = document.getElementById("decks");
//                 decks.innerHTML += `<div class="col" id="deck-${responseData['deck_id']}">
//                                         <div class="card">
//                                             <img src="#" class="card-img-top" style="height: 15rem;" alt="Image"> 
//                                             <div class="card-body">
//                                                 <h5 class="card-title">${responseData['deck_name']}</h5>
//                                                 <a href="#" class="btn btn-primary">Practice</a> 
//                                                 <a href="/edit-deck/${responseData['deck_id']}" class="btn btn-success">Edit</a>
//                                                 <button type="button" id="${responseData['deck_id']}" class="delete-deck btn btn-danger">Delete</button>
//                                             </div>
//                                         </div>
//                                     </div>`       
//             })
//     });//Try to see if there's a better way to do this without passing explicit HTML
// }

//Delete deck from user workspace
const deleteDecks = document.querySelectorAll('button.delete-deck');

for (const deck of deleteDecks) {
    deck.addEventListener('click', (evt) => {

        evt.preventDefault()

        const deck_id = evt.target.id;
        const url = `/delete-deck/${deck_id}`;

        fetch(url, {
            method: 'DELETE',
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.text())
            .then((responseData) => {
                if(responseData == 'Successful deletion!'){
                    console.log(responseData);
                    const deck = document.getElementById(`deck-${deck_id}`);
                    deck.style.display = 'none';
                }
            });
    });
};


//Update deck information in design space
const updateDeck = document.querySelector('form.update-deck');

if(updateDeck){
    updateDeck.addEventListener('submit', (evt) =>{

        evt.preventDefault();

        const deck_id = evt.target.id
        const url = `/edit-deck/${deck_id}`

        const imgInput = document.querySelector('input[type="file"]');
        const deck_name = document.getElementById('deck_name').value;
        const deck_img = imgInput.files[0]

        console.log(deck_name)

        const formData = new FormData();
        formData.append('deck_img', deck_img)
        formData.append('deck_name', deck_name)


        // for (var pair of formData.entries()) {
        //     console.log(pair[0]+ ', ' + pair[1]); 
        // }
        
        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                const deckName = document.getElementById('title');
                deckName.innerHTML = `<h2>${responseData['deck_name']} Deck Design Space</h2>
                                      <a href="/workspace">Return to your decks</a>`
            })

    });
}


//######################################################################### Flashcard requests
//BLOCK#2: Create a deck asynchrounously through AJAX without having to return HTLM code. Once
//implemented, this request hopefully also allows you to delete decks asynchrounously. So far, when you 
//create an async deck with the request below, it seems like "the way in which the deck is created"
//interferes with you deleting the new deck asynchrounously as well. What's supposed to be an async deletion 
//takes effect after you reload the page, which, if you think about it, defeats the purpose of AJAX. -------> I figured it out!

//The reason why the above happens is because when we create a new deck or flashcard, and try to delete it, the process of adding an
//eventListenier to the button never happens, this process only occurs when we navigate to /edit-deck/<deck_id>. We will try to solve this
//moving forward.

//Add new flashcard to deck in design space
// const createFlashcard = document.getElementById('create-flashcard');

// if(createFlashcard){
//     createFlashcard.addEventListener('submit', (evt) =>{

//         evt.preventDefault();

//         const formInputs = {
//             front_content: document.getElementById("front").value,
//             back_content: document.getElementById("back").value,
//         };
        
//         fetch('/create-flashcard', {
//             method: 'POST',
//             body: JSON.stringify(formInputs),
//             headers: {'Content-Type' : 'application/json',},
//         })
//             .then((response) => response.json())
//             .then((responseData) => {
//                 console.log(responseData);
//                 const flashcards = document.getElementById('flashcard-section');
//                 flashcards.innerHTML += `<li class="list-group-item" id="flashcard-${responseData['flashcard_id']}" style="display:block;" >
//                                             <h4>${responseData['front_content']}</h4>
//                                             <button type="button" class="delete-flashcard btn btn-danger" id="${responseData['flashcard_id']}">Delete</button>
//                                             <button type="button" class="btn btn-success">Edit</button>
//                                         </li>`;
//             })

//     });
// }


//Delete flashcard from user deck and design space
const deleteFlashcards = document.querySelectorAll('button.delete-flashcard');

for (const flashcard of deleteFlashcards) {
    flashcard.addEventListener('click', (evt) => {

        const flashcard_id = evt.target.id;
        const url = `/delete-flashcard/${flashcard_id}`;

        fetch(url, {
            method: 'DELETE',
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.text())
            .then((responseData) => {
                if(responseData == 'Successful deletion!'){
                    const flashcardListItem = document.getElementById(`flashcard-${flashcard_id}`);
                    flashcardListItem.style.display = 'none';
                }
            });
    });
};


//Update deck information in design space
const updateFlashcards = document.querySelectorAll('form.update-flashcard');

for(const flashcard of updateFlashcards){
    flashcard.addEventListener('submit', (evt) =>{

        evt.preventDefault();

        const flashcard_id = evt.target.id;
        const url = `/edit-flashcard/${flashcard_id}`;
        console.log(flashcard_id);
        const formInputs = {
            front_content: document.getElementById(`front_update-${flashcard_id}`).value,
            back_content: document.getElementById(`back_update-${flashcard_id}`).value,
        };

        console.log(formInputs);
        
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                const flashcardName = document.getElementById(`flashcard-title-${flashcard_id}`);
                flashcardName.innerHTML = `<h4 id="flashcard-title" style="display: inline;">${responseData['front_content']}</h4>`
            })

    });
}

