/**
 * DevOps Bookshelf - Client Interaction & UX Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    // 2. Validate checkout form before submission
    const checkoutForm = document.querySelector('.order-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', (e) => {
            const name = document.getElementById('customer_name');
            const email = document.getElementById('customer_email');
            const address = document.getElementById('customer_address');

            if (name && !name.value.trim()) {
                e.preventDefault();
                alert('Please enter your full name.');
                name.focus();
                return;
            }

            if (email && !email.value.trim()) {
                e.preventDefault();
                alert('Please enter your email address.');
                email.focus();
                return;
            }

            if (address && !address.value.trim()) {
                e.preventDefault();
                alert('Please enter your delivery address.');
                address.focus();
                return;
            }
        });
    }

    // 3. Smooth scroll for devops pill anchor
    const devopsPill = document.querySelector('.devops-pill');
    if (devopsPill) {
        devopsPill.addEventListener('click', (e) => {
            const target = document.getElementById('devops-badge-footer');
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
});
