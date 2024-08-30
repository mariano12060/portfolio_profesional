// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.querySelector('.nav-toggle');
    const navList = document.querySelector('nav ul');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            if (navList.style.display === 'block') {
                navList.style.display = 'none';
            } else {
                navList.style.display = 'block';
            }
        });
    }
});








document.addEventListener('DOMContentLoaded', function () {
    const stylePanel = document.getElementById('style-panel');
    const styleIcon = document.getElementById('style-icon');
    const closePanelButton = document.getElementById('close-style-panel');

    styleIcon.addEventListener('click', function () {
        stylePanel.classList.add('show');
    });

    closePanelButton.addEventListener('click', function () {
        stylePanel.classList.remove('show');
    });

    document.querySelectorAll('#style-panel input[type="radio"]').forEach(function (radio) {
        radio.addEventListener('change', function () {
            document.body.className = this.value;
        });
    });
});
