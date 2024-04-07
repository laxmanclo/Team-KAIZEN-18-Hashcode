document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const submitButton = document.getElementById('submitButton');
    const output = document.getElementById('output');

    fileInput.addEventListener('change', function(event) {
        previewContainer.innerHTML = ''; // Clear previous previews

        const files = event.target.files;
        for (const file of files) {
            const reader = new FileReader();

            reader.onload = function(event) {
                const previewElement = document.createElement(file.type.startsWith('image') ? 'img' : 'video');
                previewElement.src = event.target.result;
                previewElement.controls = true;
                previewContainer.appendChild(previewElement);
            };

            reader.readAsDataURL(file);
        }
    });

    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        const formData = new FormData();
        const files = fileInput.files;

        for (const file of files) {
            formData.append('files', file);
        }

        fetch('/process_data', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            output.innerHTML = '<h2>AI Model Output:</h2>' + data.output;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
