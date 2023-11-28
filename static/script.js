function startServer() {
    fetch('/start_server')
        .then(response => {
            if (response.ok) {
                window.location.href = '/server_started'; // Redirect to a new page
            } else {
                console.error('Server start request failed');
            }
        })
        .catch(error => console.error('Error:', error));
}

function startClient() {
    fetch('/start_client')
        .then(response => {
            if (response.ok) {
                window.location.href = '/client_started'; // Redirect to a new page
            } else {
                console.error('Client start request failed');
            }
        })
        .catch(error => console.error('Error:', error));
}
