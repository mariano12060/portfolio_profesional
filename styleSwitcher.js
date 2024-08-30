document.addEventListener('DOMContentLoaded', function() {
    const stylePanel = document.getElementById('style-panel');
    const styleIcon = document.getElementById('style-icon');
    const closeStylePanel = document.getElementById('close-style-panel');
    const styleRadios = document.querySelectorAll('input[name="style"]');
    const body = document.body;

    // Verificar si hay un estilo guardado en localStorage
    const savedStyle = localStorage.getItem('selectedStyle');
    if (savedStyle) {
        body.className = savedStyle;
        document.querySelector(`input[name="style"][value="${savedStyle}"]`).checked = true;
    }

    // Cambiar el estilo cuando el usuario selecciona uno diferente
    styleRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            const selectedStyle = this.value;
            body.className = selectedStyle;

            // Guardar el estilo seleccionado en localStorage
            localStorage.setItem('selectedStyle', selectedStyle);
        });
    });

    // Mostrar y ocultar el panel de estilos
    styleIcon.addEventListener('click', function() {
        stylePanel.classList.add('show');
    });

    closeStylePanel.addEventListener('click', function() {
        stylePanel.classList.remove('show');
    });
});