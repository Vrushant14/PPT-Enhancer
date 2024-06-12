document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const messageContainer = document.getElementById('message-container');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const username = document.getElementById('userid').value.trim();
        const password = document.getElementById('password').value.trim();

        if (username === '' || password === '') {
            displayMessage('Please enter both username and password.');
            return;
        }

        loginUser(username, password);
    });

    function loginUser(username, password) {
        fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: new URLSearchParams({
                'username': username,
                'password': password
            }),
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                displayMessage('Login successful.', 'success');
                window.location.href = '/entry/'; // Redirect to entry page after successful login
            } else {
                displayMessage('Invalid credentials. Please try again.', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            displayMessage('An error occurred. Please try again later.', 'error');
        });
    }

    function displayMessage(message, messageType) {
        messageContainer.textContent = message;
        messageContainer.classList.remove('success', 'error');
        if (messageType === 'success') {
            messageContainer.classList.add('success');
        } else if (messageType === 'error') {
            messageContainer.classList.add('error');
        }
    }

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
