document.getElementById('browse-link').addEventListener('click', function() {
    document.getElementById('video-upload').click();
});

document.getElementById('video-upload').addEventListener('change', function() {
    const videoFile = document.getElementById('video-upload').files[0];
    if (videoFile) {
        const videoElement = document.getElementById('video');
        const url = URL.createObjectURL(videoFile);
        videoElement.src = url;
        videoElement.style.display = 'block';
        document.getElementById('detect-btn').style.display = 'block';
    }
});

document.getElementById('upload-btn').addEventListener('click', function() {
    const videoFile = document.getElementById('video-upload').files[0];
    if (!videoFile) {
        alert('Please upload a video first.');
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Video uploaded successfully. Click "Start Detection" to analyze.</p>';
    document.getElementById('detect-btn').style.display = 'block';
    document.getElementById('stop-btn').style.display = 'block';
    document.getElementById('upload-btn').style.display = 'none';
    document.getElementById('video-upload').style.display = 'none';
    document.getElementById('browse-link').style.display = 'none';
});

document.getElementById('detect-btn').addEventListener('click', function() {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Analyzing video...</p>';

    setTimeout(() => {
        const detected = Math.random() > 0.5;
        resultDiv.innerHTML = detected 
            ? '<p>Fire detected in the video.</p>'
            : '<p>No fire detected in the video.</p>';
    }, 2000);
});

document.getElementById('stop-btn').addEventListener('click', function() {
    const resultDiv = document.getElementById('result');
    const videoElement = document.getElementById('video');
    videoElement.pause();
    videoElement.currentTime = 0;
    videoElement.style.display = 'none';

    document.getElementById('video-upload').value = '';
    document.getElementById('detect-btn').style.display = 'none';
    document.getElementById('stop-btn').style.display = 'none';
    document.getElementById('upload-btn').style.display = 'block';
    document.getElementById('video-upload').style.display = 'block';
    document.getElementById('browse-link').style.display = 'inline';
    resultDiv.innerHTML = '';
});
