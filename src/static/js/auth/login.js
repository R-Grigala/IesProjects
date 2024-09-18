function login(event) {
    event.preventDefault();  // Prevent the form from submitting

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;

    // Create a JSON object with the form values
    const formData = {
        email: email,
        password: password
    };

    fetch('http:127.0.0.1:8000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Save the token in local storage
            sessionStorage.setItem('access_token', data.access_token);
            sessionStorage.setItem('refresh_token', data.refresh_token);
            sessionStorage.setItem('user_email', email);

            // Redirect to /projects page
            window.location.href = '/projects';
        } else {
            showAlert('danger', data.error || ' გაუმართავი ავტორიზაცია.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Attach the login function to the form's submit event
document.getElementById('loginForm').onsubmit = login;
