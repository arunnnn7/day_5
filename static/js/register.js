// Form Validation using jQuery for Registration
$(document).ready(function() {

    $('#registerForm').on('submit', function(e) {
        // Clear previous error messages
        $('#error-msg').hide().text('');

        // Get values from form inputs
        let name = $('#name').val().trim();
        let email = $('#email').val().trim();
        let age = $('#age').val().trim();
        let gender = $('input[name="gender"]:checked').val();
        let course = $('#course').val();
        let password = $('#password').val();

        // 1. Required fields validation using if conditions
        if (name === '') {
            e.preventDefault();
            alert('Please enter your full name.');
            $('#error-msg').text('Full Name is required.').fadeIn();
            $('#name').focus();
            return false;
        }

        if (email === '') {
            e.preventDefault();
            alert('Please enter your email.');
            $('#error-msg').text('Email is required.').fadeIn();
            $('#email').focus();
            return false;
        }

        if (age === '') {
            e.preventDefault();
            alert('Please enter your age.');
            $('#error-msg').text('Age is required.').fadeIn();
            $('#age').focus();
            return false;
        }

        // 2. Numeric age validation using if conditions
        if (isNaN(age) || parseInt(age) <= 0) {
            e.preventDefault();
            alert('Age must be a valid positive number.');
            $('#error-msg').text('Please enter a valid numeric age.').fadeIn();
            $('#age').focus();
            return false;
        }

        if (!gender) {
            e.preventDefault();
            alert('Please select your gender.');
            $('#error-msg').text('Gender is required.').fadeIn();
            return false;
        }

        if (!course || course === '') {
            e.preventDefault();
            alert('Please select your course.');
            $('#error-msg').text('Course selection is required.').fadeIn();
            $('#course').focus();
            return false;
        }

        // 3. Password length validation (>= 6) using if conditions
        if (password === '') {
            e.preventDefault();
            alert('Please enter a password.');
            $('#error-msg').text('Password is required.').fadeIn();
            $('#password').focus();
            return false;
        }

        if (password.length < 6) {
            e.preventDefault();
            alert('Password must be at least 6 characters long.');
            $('#error-msg').text('Password must be at least 6 characters long.').fadeIn();
            $('#password').focus();
            return false;
        }

        // All checks passed
        return true;
    });

});
