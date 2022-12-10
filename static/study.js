window.addEventListener("DOMContentLoaded", function() {
    console.log("Javascript file successfully linked to HTML")
    loadPieces();
});

async function loadPieces(){

    fetch("https://allarassemjonathan.github.io/api/file.json")
    .then(validateJSON)
    .then(pieceList => {
        console.log(pieceList)
        let ol = document.getElementById("main");
        for (const key in pieceList) {
            let pieceLi = document.createElement('div');
            pieceLi.setAttribute('id', pieceList[key].title + " list");
            pieceLi.setAttribute('class', "");
            ol.append(pieceLi);

            let pieceDiv = document.createElement('div');
            pieceDiv.setAttribute('id', pieceList[key].title + " div");
            pieceLi.append(pieceDiv);
            pieceDiv.innerText = pieceList[key].title

            let pieceButton = document.createElement('button');
            pieceButton.setAttribute('id', pieceList[key].title + " button");
            pieceButton.addEventListener('click', function() {
                renderPiece(pieceList[key]);
            });
            pieceButton.innerText = "Maximize";
            pieceLi.append(pieceButton);
        }
    });
}

function renderPiece(i) {
    let buttonClicked = document.getElementById(i.title + " button");
    // expand div
    if(buttonClicked.innerText == "Maximize") {
        let pieceDiv = document.getElementById(i.title + " div");
        pieceDiv.innerHTML = "";

        let pieceHeader = document.createElement('h4');
        pieceHeader.setAttribute('id', i.title + " header");
        pieceHeader.innerText = i.title + " by " + i.artist;

        let pieceDate = document.createElement('p');
        pieceDate.setAttribute('id', i.title + " date");
        pieceDate.innerText = Math.abs(i.year[0]) + "-" + Math.abs(i.year[1]);
        if(i.year[0] < 0) {
            pieceDate.innerText += " B.C.";
        } else {
            pieceDate.innerText += " A.D.";
        }

        let pieceImage = document.createElement('img');
        pieceImage.setAttribute('id', i.title + " image");
        pieceImage.setAttribute('width', '400px');
        pieceImage.setAttribute('src', '..\\static\\Artworks Database\\Artpieces\\' + i.title + ".jpg");
        pieceImage.setAttribute('alt', i.title);

        pieceDiv.append(pieceHeader);
        pieceDiv.append(pieceDate);
        pieceDiv.append(pieceImage);
        buttonClicked.innerText = "Minimize";
    // reduce div
    } else {
        let pieceDiv = document.getElementById(i.title + " div");
        pieceDiv.innerHTML = "";
        pieceDiv.innerText = i.title;
        buttonClicked.innerText = "Maximize";
    }
    let script = document.getElementById('srcScript');
    console.log(script[src]);
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
 function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}