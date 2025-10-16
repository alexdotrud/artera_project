from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents
from shop.models import Artwork
from .models import OrderItem, Order
from profiles.models import Profile

import stripe
import json

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': getattr(request.user, 'username', ''),
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)
    
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user  
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            for item_id, item_data in bag.items():
                artwork = get_object_or_404(Artwork, pk=item_id)

                if isinstance(item_data, int):
                    OrderItem.objects.create(
                        order=order,
                        artwork=artwork,
                        quantity=item_data,
                    )
                else:
                    for size, quantity in item_data['items_by_size'].items():
                        OrderItem.objects.create(
                            order=order,
                            artwork=artwork,
                            quantity=quantity,
                            size=size,
                        )
            order.update_total()
            if request.user.is_authenticated and ('save-info' in request.POST):
               profile, _ = Profile.objects.get_or_create(user=request.user)
               profile.full_name = request.POST.get('full_name', '').strip()
               profile.phone_number = request.POST.get('phone_number', '').strip()
               profile.address_line_delivery = request.POST.get('street_address1', '').strip()
               profile.address_line_living = request.POST.get('street_address2', '').strip()
               profile.city = request.POST.get('town_or_city', '').strip()
               profile.postal_code = request.POST.get('postcode', '').strip()
               profile.country = request.POST.get('country', '').strip()
               profile.save()

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            return redirect(reverse('checkout'))
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('all_artworks'))
        
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        initial = {}
        if request.user.is_authenticated:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            initial = {
                'full_name': profile.full_name or '',
                'email': request.user.email or '',
                'phone_number': profile.phone_number or '',
                'country': profile.country or '',
                'postcode': profile.postal_code or '',
                'town_or_city': profile.city or '',
                'street_address1': profile.address_line_delivery or '',
                'county': profile.country or '',
            }
        order_form = OrderForm(initial=initial) 

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)
    
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)