document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('nav a');
    const currentLocation = window.location.pathname;

    navLinks.forEach(link => {
        if (link.href.includes(`${currentLocation}`)) {
            link.classList.add('active');
        }
    });

    const form = document.getElementById('verify-form');
    if (form) {
        form.addEventListener('submit', async function(event) {
            event.preventDefault();
            const userId = document.getElementById('user_id').value;
            const documents = document.getElementById('documents').files;
            if (!userId || documents.length === 0) {
                alert('Please fill in all fields.');
                return;
            }
            const formData = new FormData();
            formData.append('user_id', userId);
            for (let i = 0; i < documents.length; i++) {
                formData.append('documents', documents[i]);
            }
            const response = await fetch('/api/verify', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            alert(result.status);
        });
    }

    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
});
