document.getElementById('generateButton').addEventListener('click', function() {
    var promptText = document.getElementById('imageRequest').value.trim();
    

    var addVesper = document.getElementById('vesperToggle').checked;

    var requestData = {
        text: promptText,
        addVesper: addVesper
    };

    // Check if the prompt is empty and alert the user if it is
    if (!promptText) {
        alert('Please enter a prompt.');
        return; // Stop the function if the prompt is empty
    }

    // Show the spinner
    document.getElementById('spinner').style.display = 'flex';
    
    // Send the request to the server
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify({
            prompt: promptText, // Ensure this is the variable holding the user's prompt
            addVesper: addVesper // The state of the addVesper toggle
        })
        //body: JSON.stringify(requestData) 
        //body: JSON.stringify({prompt: promptText})  Send the prompt text under the key 'prompt'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        var img = new Image();
        img.onload = function() {
            // Hide the spinner when the image is loaded
            document.getElementById('spinner').style.display = 'none';
        };
        img.src = data.imageUrl; // Make sure this matches the key in your response
        document.getElementById('imageDisplay').innerHTML = '';
        document.getElementById('imageDisplay').appendChild(img);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        document.getElementById('spinner').style.display = 'none';
        alert(error.message); // Optionally alert the user
    });
});

document.getElementById('clearButton').addEventListener('click', function() {
    // Clear the text area
    document.getElementById('imageRequest').value = '';

    // Hide the spinner
    document.getElementById('spinner').style.display = 'none';

    // Clear the image display area
    document.getElementById('imageDisplay').innerHTML = '';
});
