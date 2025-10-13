from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('all_artworks'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key' : 'pk_test_51SAVStPhwAejrPKsQFc7VR7sxnYjDf4ENfohFhwMqcDu1geZDJLSQYvxRXZhYPMdFFCKGIZRvVzysj0YCGbtU6Gz002jbwYeWI',
    }

    return render(request, template, context)