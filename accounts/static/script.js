document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        const formData = new FormData(form); // Create a FormData object to send form data including files

        // Send a POST request to the server to handle form submission
        fetch('/upload/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token in the request headers
            },
        })
        .then(response => {
            if (response.ok) {
                // Handle successful response, e.g., show a success message
                alert('Presentation uploaded and enhanced successfully!');
            } else {
                // Handle error response, e.g., display an error message
                alert('Error uploading and enhancing presentation. Please try again.');
            }
        })
        .catch(error => {
            // Handle fetch error, e.g., display an error message
            console.error('Error:', error);
            alert('An error occurred while processing the request. Please try again later.');
        });
    });

    // Function to retrieve CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
