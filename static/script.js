document.getElementById('copy').addEventListener('click', function() {
    const shortUrlInput = document.getElementById('shorturl');
    if (shortUrlInput.value) {
        navigator.clipboard.writeText(shortUrlInput.value)
            .then(() => {
                const copyBtn = document.getElementById('copy');
                const originalColor = copyBtn.style.backgroundColor;
                copyBtn.style.backgroundColor = '#4CAF50'; 
                alert('Copied to clipboard!');
                setTimeout(() => {
                    copyBtn.style.backgroundColor = originalColor;
                }, 1000);
            })
            .catch(err => {
                console.error('Error copying text: ', err);
            });
    } else {
        alert('Nothing to copy yet!');
    }
});

document.getElementById('clear').addEventListener('click', function() {
    document.getElementById('shorturl').value = ''; 
});