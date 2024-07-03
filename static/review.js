document.getElementById('review-ad-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const advertiseId = document.getElementById('advertise-id').value;
    const status = document.getElementById('status').value;

    try {
        const response = await fetch(`/support/advertise/${advertiseId}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status })
        });

        const result = await response.json();
        document.getElementById('review-message').textContent = result.message;
    } catch (error) {
        document.getElementById('review-message').textContent = 'An error occurred';
    }
});
