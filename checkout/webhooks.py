from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler  # same app -> relative import
import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    wh_secret = settings.STRIPE_WH_SECRET

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    if not sig_header:
        return HttpResponseBadRequest("Missing Stripe signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        # Invalid payload
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponseBadRequest("Invalid signature")

    # Connect to handler
    handler = StripeWH_Handler(request)
    event_map = {
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }
    event_handler = event_map.get(event["type"], handler.handle_event)
    return event_handler(event)
