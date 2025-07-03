// // JavaScript for polling events - will be implemented in Phase 5
// console.log('GitHub Webhook Monitor loaded');



function fetchEvents() {
    fetch('/api/events')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('events-container');
            container.innerHTML = '';

            if (data.events && data.events.length > 0) {
                data.events.forEach(event => {
                    const p = document.createElement('p');
                    p.textContent = event.message;
                    container.appendChild(p);
                });
            } else {
                container.innerHTML = '<p>No events yet.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching events:', error);
        });
}

// Poll every 15 seconds
setInterval(fetchEvents, 15000);
window.onload = fetchEvents;
