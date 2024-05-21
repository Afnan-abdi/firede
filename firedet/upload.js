document.getElementById('browse-link').addEventListener('click', function() {
    document.getElementById('image-upload').click();
});

document.getElementById('upload-btn').addEventListener('click', function() {
    const upload = document.getElementById('image-upload').files[0];
    if (!upload) {
        alert('Please upload an image first.');
        return;
    }

    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Analyzing image...</p>';
    
    setTimeout(() => {
        const detected = Math.random() > 0.5;
        resultDiv.innerHTML = detected 
            ? '<p>Fire detected in the image.</p>'
            : '<p>No fire detected in the image.</p>';
    }, 2000);
});
