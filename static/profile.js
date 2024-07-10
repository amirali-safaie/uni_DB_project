document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    const messageDiv = document.getElementById('message');

    profileForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData();

        // Only add fields that have been filled out
        const inputs = profileForm.querySelectorAll('input:not([type="file"])');
        inputs.forEach(input => {
            if (input.value) {
                formData.append(input.name, input.value);
            }
        });

        // Handle file upload
        const fileInput = document.getElementById('profile_image');
        if (fileInput.files.length > 0) {
            formData.append('profile_image', fileInput.files[0]);
        }

        // First, update the profile information
        fetch('/user/1/profileChanges', {
            method: 'PATCH',
            body: JSON.stringify(Object.fromEntries(formData)),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update profile');
            }
            return response.json();
        })
        .then(data => {
            // If there's a file to upload, do it after successful profile update
            if (fileInput.files.length > 0) {
                const imageFormData = new FormData();
                imageFormData.append('file', fileInput.files[0]);

                return fetch('/user/1/upload-profile-image', {
                    method: 'POST',
                    body: imageFormData
                });
            } else {
                return Promise.resolve({ ok: true, json: () => ({ message: 'Profile updated successfully' }) });
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to upload image');
            }
            return response.json();
        })
        .then(data => {
            // Show success message
            messageDiv.textContent = 'Profile updated successfully';
            messageDiv.style.display = 'block';

            // Optional: Reset the form after successful submission
            profileForm.reset();
        })
        .catch(error => {
            // Show error message
            messageDiv.textContent = 'An error occurred. Please try again.';
            messageDiv.style.display = 'block';
            console.error('Error:', error);
        });
    });
});