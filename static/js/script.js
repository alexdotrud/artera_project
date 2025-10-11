function Cahnge() {
    const select = document.getElementById('id_product_size');
    const priceEl = document.getElementById('priceDisplay');
    if (!select || !priceEl) return;
    const fmt = v => '$' + (Number(v || 0)).toFixed(2);

    function update() {
        const opt = select.options[select.selectedIndex];
        priceEl.textContent = fmt(opt.dataset.price);
    }
    select.addEventListener('change', update);
    update();
};