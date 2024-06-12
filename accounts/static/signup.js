document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');
    const signupButton = document.getElementById('signup-button');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        const confirmPassword = document.getElementById('confirm_password').value.trim();

        const passwordValidationMessage = validatePassword(password);
        if (passwordValidationMessage !== "") {
            alert(passwordValidationMessage);
            return;
        }

        if (username === '' || email === '' || password === '' || confirmPassword === '') {
            alert('All fields are required');
            return;
        }

        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }

        // Perform signup action here
        signupButton.disabled = true;
        signupButton.classList.add('disabled');
        redirectToLogin();
    });

    signupButton.addEventListener('click', function(event) {
        // Trigger the form submission manually
        signupForm.submit();
    });

    function redirectToLogin() {
        window.location.href = "/login/";
    }

    function validatePassword(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasNumber = /\d/.test(password);

        if (password.length < minLength) {
            return "Password must be at least 8 characters long.";
        }

        if (!hasUpperCase) {
            return "Password must contain at least one uppercase letter.";
        }

        if (!hasNumber) {
            return "Password must contain at least one number.";
        }

        return ""; // Password is valid
    }
});
