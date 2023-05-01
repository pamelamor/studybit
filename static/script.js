'use strict';

import {Application} from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);
app
    .load('https://prod.spline.design/cjO2PR-vuPfOFfea/scene.splinecode')
    // .then(() => {
	// 	app.setZoom(1.0);
	// });

//###################################################################### DECK
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



//Display deck image being uploaded
function preview(){
    uploaded_image.src=URL.createObjectURL(event.target.files[0]);
}


function preview_card(){
    const deck_color = document.getElementById("deck_color").value;
    const deck_font = document.getElementById("deck_font").value;
    const font_color = document.getElementById("deck_font_color").value;
    const google_link = document.querySelector("#google_fonts");
    console.log(google_link)
    google_link.href = `https://fonts.googleapis.com/css2?family=${deck_font}`;
    card_display.style.backgroundColor = deck_color
    card_display.style.fontFamily = `${deck_font}`
    card_display.style.color = font_color
}


//Update deck information in design space
const updateDeck = document.querySelector('form.update-deck');
if(updateDeck){
    updateDeck.addEventListener('submit', (evt) =>{

        evt.preventDefault();

        const deck_id = evt.target.id
        const url = `/edit-deck/${deck_id}`
        const formData = new FormData();
        const imgDeck = document.querySelector('.update-deck input[type="file"]');
        console.log(imgDeck)
        let deck_img = imgDeck.files[0]
        console.log(deck_img)

        if(deck_img == undefined){
            deck_img = new File([""], "dummyfile.png", {type: "img/png", lastModified: new Date(0)});
        }

        const deck_name = document.getElementById('deck_name').value;
        const deck_font = document.getElementById('deck_font').value;
        console.log(deck_font)
        const deck_color = document.getElementById('deck_color').value;
        const deck_font_color = document.getElementById('deck_font_color').value;


        formData.append('deck_img', deck_img)
        formData.append('deck_name', deck_name)
        formData.append('deck_font', deck_font)
        formData.append('deck_color', deck_color)
        formData.append('deck_font_color', deck_font_color)

        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
            
        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                const deckName = document.getElementById('title');
                deckName.innerHTML = `<h2>${responseData['deck_name']} Deck Design Space</h2>
                                      <a href="/workspace">Return to your decks</a>`;
            });
    });
}

//###################################################################### FLASHCARD
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


//Display flashcard image being uploaded
function preview_img(id){
    const flashcard_img = document.getElementById(`uploaded_card_image_${id}`);
    flashcard_img.src=URL.createObjectURL(event.target.files[0]);
}


//Update flashcard information in design space
const updateFlashcards = document.querySelectorAll('form.update-flashcard');

for(const flashcard of updateFlashcards){
    flashcard.addEventListener('submit', (evt) =>{

        evt.preventDefault();

        const flashcard_id = evt.target.name;
        console.log(flashcard_id)
        const url = `/edit-flashcard/${flashcard_id}`;
        const formData = new FormData();
        const imgCard = document.querySelector(`#${evt.target.id} input[type="file"]`);
        console.log(imgCard)
        let flashcard_img = imgCard.files[0]
        console.log(flashcard_img)

        if(flashcard_img == undefined){
            flashcard_img = new File([""], "dummyfile.png", {type: "img/png", lastModified: new Date(0)});
        }

        const front_content = document.getElementById(`front_update-${flashcard_id}`).value;
        const back_content = document.getElementById(`back_update-${flashcard_id}`).value;


        formData.append('front_content', front_content)
        formData.append('back_content', back_content)
        formData.append('flashcard_img', flashcard_img)


        for (var pair of formData.entries()) {
            console.log(pair[0]+ ', ' + pair[1]); 
        }
        
        fetch(url, {
            method: 'POST',
            body: formData,
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log(responseData);
                const flashcardName = document.getElementById(`flashcard-title-${flashcard_id}`);
                flashcardName.innerHTML = `<h4 id="flashcard-title" style="display: inline;">${responseData['front_content']}</h4>`
            })

    });
}


//Flip card in study session 
const card = document.querySelector('.card_inner');
if(card){
    card.addEventListener('click', () => {

        console.log("Card clicked!");
        card.classList.toggle('is-flipped')
    });
}


//Switch the following card in the stack and collect user answer data 
const nextBtn = document.querySelector('.next');

if(nextBtn){
    nextBtn.addEventListener('click', (evt) =>{

        evt.preventDefault();
        const deck_id = evt.target.id;
        const url = `/study-session/${deck_id}`

        
        const formInputs = {
            i: document.getElementById('front_content').getAttribute('name')
        }
        

        fetch(url, {
            method: 'POST',
            body: JSON.stringify(formInputs),
            headers: {'Content-Type' : 'application/json',},
        })
            .then((response) => response.json())
            .then((responseData) => {
                if(responseData['msg']){
                    console.log(responseData['msg']);
                    const exit = document.getElementById('exit')
                    const done = document.getElementById('finished')
                    const not_done = document.getElementById('unfinished')
                    not_done.style.display = 'none';
                    exit.style.display = 'none';
                    done.style.display = 'block';
                }
                else{
                    console.log(responseData)
                    const front = document.getElementById('front-side');
                    front.innerHTML = `<h1 class="card-title" name=${responseData['i']} id="front_content">${responseData['front']}</h1>`;
                    const back = document.getElementById('back-side');
                    back.innerHTML = `<h1 class="card-title" name=${responseData['i']} id="back_content">${responseData['back']}</h1>`;
                    const img = document.getElementById('flashcard_img');
                    console.log(img)
                    img.innerHTML = `<img src=${responseData['img']} class="card-img-top" alt="..." width="300" height="300">`;
                }  
            });
    });
}


