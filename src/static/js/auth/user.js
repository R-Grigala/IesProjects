// Open the modal for editing a User record
function openUserModal() {
    const token = localStorage.getItem('access_token');
    const emailText = document.getElementById('user_email');
    const roleText = document.getElementById('user_role');
    fetch(`/api/user`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,  // Include the JWT token
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            if (response.status === 401) {
                showAlert('alertPlaceholder', 'danger', 'სესიის ვადა ამოიწურა. გთხოვთ, თავიდან შეხვიდეთ სისტემაში.');
                clearSessionData();
            } else if (response.status === 403) {
                showAlert('alertPlaceholder', 'danger', 'არ გაქვთ უფლებები ამ მონაცემების ნახვისთვის.');
            } else {
                showAlert('alertPlaceholder', 'danger', 'მოხდა შეცდომა მონაცემების გამოთხოვისას.');
            }
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        if (data) {
            document.getElementById('userUUID').value = data.uuid;
            document.getElementById('user_name').value = data.name;
            document.getElementById('user_lastname').value = data.lastname;
            emailText.textContent = data.email;
            roleText.textContent = data.role_name;

            // Show the update button only if the role is Admin
            if (data.role_name === 'Admin') {
                accountsButton.style.display = 'block';
            }
        } else {
            showAlert('alertPlaceholder', 'danger', 'მომხმარებელი არ მოიძებნა.');
        }
    })
    .catch(error => console.error('Error fetching data:', error));


    const modal = new bootstrap.Modal(document.getElementById('UserModal'));
    modal.show();
}

// Redirect to the accounts page
function redirectToAccounts() {
    window.location.href = '/accounts';
}

function submitUserForm(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById('UserForm'));
    const UUIDField = document.getElementById('userUUID').value;

    const token = localStorage.getItem('access_token');

    // makeApiRequest is in the globalAccessControl.js
    makeApiRequest(`/api/user/${UUIDField}`, {
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    })
    .then(data => {
        if (data.error) {
            closeModal('UserModal')
            showAlert('alertPlaceholder', 'danger', data.error || ' მონაცემტა ცვლილებისას დაფიქსირდა შეცდომა');
        } else {
            window.location.reload(); // Reload the page to reflect changes
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function changePassword(){

    const user_email = document.getElementById('user_email').innerHTML;
    const changePasswordLink = document.getElementById('changePasswordLink');
    const formData = {
        modalEmail: user_email
    };

    changePasswordLink.style.pointerEvents = 'none';
    changePasswordLink.style.opacity = '0.6'; // optional visual cue
    changePasswordLink.style.cursor = 'not-allowed';

    makeApiRequest('/api/request_reset_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)

    }).then(data => {
        changePasswordLink.style.pointerEvents = 'auto';
        changePasswordLink.style.opacity = '1';
        changePasswordLink.style.cursor = 'pointer';
        if (data.message) {
            
            showAlert('alertPlaceholder', 'success', data.message || ' გთხოვთ შეამოწმოთ ელ.ფოსტა, ვერიფიკაციის ლინკი გამოგზავნილია.');
            
            // Close the modal 
                closeModal('UserModal');
        } else {

            showAlert('alertPlaceholder', 'danger', data.error || ' გაუმართავი ელ.ფოსტა.');
            closeModal('UserModal');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });


}