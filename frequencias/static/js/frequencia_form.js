// Show/hide justification field based on presence checkbox
document.addEventListener('DOMContentLoaded', function() {
    const presenteCheckbox = document.getElementById('id_presente');
    const justificativaField = document.getElementById('id_justificativa').closest('.mb-3');
    
    function toggleJustificativa() {
        if (presenteCheckbox.checked) {
            justificativaField.style.display = 'none';
        } else {
            justificativaField.style.display = 'block';
        }
    }
    
    if (presenteCheckbox) {
        toggleJustificativa();
        presenteCheckbox.addEventListener('change', toggleJustificativa);
    }
});
