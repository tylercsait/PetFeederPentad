document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/notifications');

    socket.on('connect', function() {
        console.log("Connected to the server");
    });

    socket.on('notify', function(data) {
        console.log("Received notification:", data.message);
        // Display notification message in the HTML
        let notificationElement = document.getElementById('notification');
        if (notificationElement) {
            notificationElement.innerText = data.message;
        } else {
            alert(data.message); // Fallback to alert
        }
    });

    socket.on('disconnect', function() {
        console.log("Disconnected from the server");
    });

    socket.on('error', function(error) {
        console.error("Socket.IO error:", error);
    });
});
