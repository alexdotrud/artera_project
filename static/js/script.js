document.addEventListener('DOMContentLoaded', () => {
    /*
    Collaborate Page.
    Function to show the ofeer form after pressing the collaborate button.
    */
    const el = document.getElementById('collabForm');
    const btn = document.getElementById('formToggle');
    const txt = btn.querySelector('.toggle-text');
    const chev = btn.querySelector('.chevron');

    el.addEventListener('shown.bs.collapse', () => {
        txt.textContent = 'Hide form –';
        chev.classList.add('rotate-180');
        el.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
    el.addEventListener('hidden.bs.collapse', () => {
        txt.textContent = 'Add your idea +';
        chev.classList.remove('rotate-180');
    });
});

// Show overlay immediately after clicking "Complete Order"
const overlay = document.getElementById('loading-overlay');
overlay.classList.remove('d-none');

// Disable the submit button
document.getElementById('submit-button').disabled = true;