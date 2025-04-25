document.getElementById('record-form').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/summarize', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('summary').innerText = data.summary;
    })
    .catch(error => console.error('Error:', error));
};
