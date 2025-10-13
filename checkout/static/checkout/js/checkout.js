var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();
var css = getComputedStyle(document.documentElement);
var style = {
    base: {
        color: (css.getPropertyValue('--ink') || '#1f1f1f').trim(),
        fontFamily: '"Cardo", serif',
        fontSize: '16px',
        '::placeholder': {
            color: (css.getPropertyValue('--muted') || '#6c757d').trim()
        },
        iconColor: (css.getPropertyValue('--primary-color') || '#442818').trim()
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {
    style: style
});
card.mount('#card-element');

// Real-time errors
card.on('change', function (event) {
    $('#card-errors').text(event.error ? event.error.message : '');
});