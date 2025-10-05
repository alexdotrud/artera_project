 const burger = document.getElementById('navbarToggle');
 const menu = document.getElementById('mobileMenu');
 const closeBtn = document.getElementById('CloseBtn');

 function toggleMenu() {
     menu.classList.toggle('active');
 }

 // burger opens/closes
 burger.addEventListener('click', toggleMenu);

 // ✕ button also closes (if you have one)
 if (closeBtn) closeBtn.addEventListener('click', toggleMenu);