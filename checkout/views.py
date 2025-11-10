from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django_countries import countries
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .forms import OrderForm
from .models import Order, OrderItem
from shop.models import Artwork
from bag.contexts import bag_contents
from profiles.models import Profile

import stripe
import json


def send_order_confirmation(order):
    """Send a confirmation email for a completed order."""
    site = Site.objects.get_current()
    ctx = {
        "order": order,
        "site": site,
    }

    subject = render_to_string("checkout/email/confirmation_subject.txt", ctx).strip()
    text_body = render_to_string("checkout/email/confirmation_body.txt", ctx)
    try:
        html_body = render_to_string("checkout/email/confirmation_body.html", ctx)
    except Exception:
        html_body = None

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.email],
    )
    if html_body:
        email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)

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
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)

def _country_to_code(country: str) -> str:
    """Convert a country name or code to a normalized ISO country code."""
    if not country:
        return ''
    country = str(country).strip()
    if len(country) == 2 and country.isalpha():
        return country.upper()
    for code, name in countries:
        if name.lower() == country.lower():
            return code
    return country

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
                try:
                    artwork = get_object_or_404(Artwork, id=item_id)
                    if isinstance(item_data, int):
                        order_item = OrderItem(
                            order=order,
                            artwork=artwork,
                            quantity=item_data,
                        )
                        order_item.save()
                    else:
                        sizes_dict = {}
                        if isinstance(item_data, dict):
                            if 'sizes' in item_data and isinstance(item_data['sizes'], dict):
                                sizes_dict = item_data['sizes']
                            elif 'items_by_size' in item_data and isinstance(item_data['items_by_size'], dict):
                                sizes_dict = item_data['items_by_size']

                        for size, quantity in sizes_dict.items():
                            qty = int(quantity) if quantity else 1
                            order_item = OrderItem(
                            order=order,
                            artwork=artwork,
                            quantity=qty,
                            size=size,
                        )
                            order_item.save()

                except Artwork.DoesNotExist:
                    messages.error(request, (
                        "One of the artworks in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
                
            if request.user.is_authenticated and 'save_info' in request.POST:
                profile, _ = Profile.objects.get_or_create(user=request.user)
                cd = order_form.cleaned_data
                profile.full_name = cd.get('full_name', '') or ''
                profile.phone_number = cd.get('phone_number', '') or ''
                profile.address_line_delivery = cd.get('street_address1', '') or ''
                profile.address_line_living = cd.get('street_address2', '') or ''
                profile.city = cd.get('town_or_city', '') or ''
                profile.postal_code = cd.get('postcode', '') or ''
                c = cd.get('country')
                profile.country = getattr(c, 'code', '') or '' 
                profile.save()

            request.session['save_info'] = 'save_info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
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
            country_code = _country_to_code(profile.country)
            initial = {
                'full_name': profile.full_name or '',
                'email': request.user.email or '',
                'phone_number': profile.phone_number or '',
                'country': country_code,
                'postcode': profile.postal_code or '',
                'town_or_city': profile.city or '',
                'street_address1': profile.address_line_delivery or '',
                'street_address2': profile.address_line_living or '',
                'county': '', 
            }
        order_form = OrderForm(initial=initial)

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

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
    send_order_confirmation(order)
    
    messages.success(request, f'Order successfully processed! A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)