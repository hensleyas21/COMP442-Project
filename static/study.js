window.addEventListener("DOMContentLoaded", function() {
    console.log("Javascript file successfully linked to HTML")
    loadPieces();
});
/**
 * Fetch the json file
 */
function loadPieces(){

    fetch("C:\\Users\\ALLARASSEMJJ20\\WebProject\\COMP442-Project\\static\\Artworks Database\\pieces.json")
    .then(validateJSON)
    .then(printInfo)
    .catch(error => {
        console.log("Classes fetch failed...", error)
    });
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