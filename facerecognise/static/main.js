$(document).ready(function () {
    const video = document.getElementById('video');
    const registerBtn = document.getElementById('register-btn');
    const loginBtn = document.getElementById('login-btn');

    // Get user media
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err) {
            console.error('Error accessing the camera:', err);
        });

    registerBtn.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        // Prompt user to enter their name
        const username = prompt('Enter your name:');
        if (username) {
            // Send captured image and username to the server
            $.ajax({
                url: '/register',
                type: 'POST',
                data: { username: username, image: imageData },
                success: function (response) {
                    alert(response.message);
                },
                error: function (xhr, status, error) {
                    console.error('Error registering user:', error);
                }
            });
        }
    });

    loginBtn.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');

        // Prompt user to enter their name
        const username = prompt('Enter your name:');
        if (username) {
            // Send captured image and username to the server
            $.ajax({
                url: '/login',
                type: 'POST',
                data: { username: username, image: imageData },
                success: function (response) {
                    alert(response.message);
                },
                error: function (xhr, status, error) {
                    console.error('Error logging in user:', error);
                }
            });
        }
    });
});
