let stream;

document.getElementById('camera-box').addEventListener('click', function() {
    if (!stream) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(mediaStream => {
                stream = mediaStream;
                const videoElement = document.getElementById('camera');
                videoElement.srcObject = stream;
                videoElement.style.display = 'block';
                document.querySelector('.camera-box-content').style.display = 'none';
                document.getElementById('start-detect').style.display = 'block';
            })
            .catch(err => {
                console.error('Error accessing camera: ', err);
                alert('Error accessing camera: ' + err.message);
            });
    }
});

function captureAndSendFrame() {
    const videoElement = document.getElementById('camera');
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const context = canvas.getContext('2d');

    // Capture frame
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Convert to Blob and send to server
    canvas.toBlob(function(blob) {
        const formData = new FormData();
        formData.append('file', blob, 'frame.jpg');
        
        fetch('/upload-image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = data.result ? 
                '<p>Fire detected in the video.</p>' : 
                '<p>No fire detected in the video.</p>';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, 'image/jpeg');
}

let intervalId;

document.getElementById('start-detect').addEventListener('click', function() {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Analyzing video...</p>';

    // Capture frame every 2 seconds and send to server
    intervalId = setInterval(captureAndSendFrame, 2000);

    document.getElementById('stop-detect').style.display = 'block';
    document.getElementById('start-detect').style.display = 'none';
});

document.getElementById('stop-detect').addEventListener('click', function() {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    const videoElement = document.getElementById('camera');
    videoElement.pause();
    videoElement.srcObject = null;

    stream.getTracks().forEach(track => track.stop());
    stream = null;

    clearInterval(intervalId);

    document.getElementById('stop-detect').style.display = 'none';
    document.getElementById('start-detect').style.display = 'none';
    document.querySelector('.camera-box-content').style.display = 'flex';
    videoElement.style.display = 'none';
});

document.getElementById('close-camera').addEventListener('click', function() {
    const resultDiv = document.getElementById('result');
    const videoElement = document.getElementById('camera');
    videoElement.pause();
    videoElement.srcObject = null;

    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    stream = null;

    clearInterval(intervalId);

    resultDiv.innerHTML = '';
    document.getElementById('stop-detect').style.display = 'none';
    document.getElementById('start-detect').style.display = 'none';
    document.querySelector('.camera-box-content').style.display = 'flex';
    videoElement.style.display = 'none';
});
