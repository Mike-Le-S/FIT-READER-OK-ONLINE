document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const summarySection = document.getElementById('summary-section');
    const summaryOutput = document.getElementById('summary-output');
    const copySummaryButton = document.getElementById('copy-summary-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorSection = document.getElementById('error-section');
    const errorOutput = document.getElementById('error-output');

    // --- Drag and Drop --- 
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault(); // Prevent default behavior (Prevent file from being opened)
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.classList.remove('dragover');
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // --- File Input Click --- 
    fileInput.addEventListener('change', (event) => {
        const files = event.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    // Trigger file input when drop zone is clicked (excluding the actual input button)
    dropZone.addEventListener('click', (event) => {
        if (event.target !== fileInput && event.target.tagName !== 'LABEL') {
            fileInput.click();
        }
    });

    // --- File Handling --- 
    function handleFile(file) {
        if (!file.name.toLowerCase().endsWith('.fit')) {
            displayError('Type de fichier invalide. Veuillez charger un fichier .fit');
            return;
        }

        loadingIndicator.style.display = 'block';
        summarySection.style.display = 'none';
        errorSection.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingIndicator.style.display = 'none';
            if (data.error) {
                displayError(data.error);
            } else {
                summaryOutput.textContent = data.summary; // data.summary est déjà le texte formaté
                summarySection.style.display = 'block';
                if (data.errors && data.errors.length > 0) {
                    console.warn("Erreurs de décodage du SDK FIT:", data.errors);
                    // Afficher un avertissement mineur si nécessaire
                }
            }
        })
        .catch(error => {
            loadingIndicator.style.display = 'none';
            displayError('Erreur de communication avec le serveur. Veuillez réessayer.');
            console.error('Error uploading file:', error);
        });
    }

    // --- Copy Summary --- 
    copySummaryButton.addEventListener('click', () => {
        navigator.clipboard.writeText(summaryOutput.textContent)
            .then(() => {
                // Peut-être afficher une petite notification de succès
                alert('Résumé copié dans le presse-papiers !');
            })
            .catch(err => {
                console.error('Failed to copy summary: ', err);
                alert('Erreur lors de la copie du résumé.');
            });
    });
    
    // --- Error Display --- 
    function displayError(message) {
        errorOutput.textContent = message;
        errorSection.style.display = 'block';
        summarySection.style.display = 'none';
    }
});
