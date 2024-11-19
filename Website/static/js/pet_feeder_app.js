// app.js
document.getElementById('pet-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const rfid = document.getElementById('rfid').value;
    const rfid_text = document.getElementById('rfid_text').value;
    const max_feedings_day = document.getElementById('max_feedings_day').value;
    const portions_per_feeding = document.getElementById('portions_per_feeding').value;

    const response = await fetch('/api/pets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rfid, rfid_text, max_feedings_day, portions_per_feeding })
    });

    if (response.ok) {
        alert('Pet information submitted successfully!');
    } else {
        alert('Failed to submit pet information.');
    }
});