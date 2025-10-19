document.addEventListener('DOMContentLoaded', () => {
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