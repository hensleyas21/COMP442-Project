window.addEventListener("DOMContentLoaded", function() {
    console.log("Javascript file successfully linked to HTML")
    loadPieces();
});
/**
 * Fetch the json file
 */
async function loadPieces(){

    fetch("https://allarassemjonathan.github.io/api/file.json")
    .then(validateJSON)
    .then(pieceList => {
        let masterDiv = document.getElementById("main");
        for (key in pieceList) {
            
        }
    });
}
/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {ClassAPIResource} data HTTP response to be checked
 */
function printInfo(data){
    console.log(data);
    const div_main = document.getElementById("main");

    for (const element of data.results){
        div_ref = document.createElement("li");
        div_ref.innerText = element.title;
        div_main.appendChild(div_ref);
    }
    
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