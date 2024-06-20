from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ShippingAddress
from .forms import ShippingForm
import stripe
import stripe
from django.contrib import messages
from item.models import Order 
from item.models import Item 
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY



@login_required
def shipping_details(request):
    item_id = request.GET.get('item_id')
    item = get_object_or_404(Item, id=item_id)  # Fetch the item based on ID

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_details = form.save(commit=False)
            shipping_details.user = request.user
            shipping_details.save()
            return redirect('billing:payment', item_id=item_id)  # Pass item_id to payment view
    else:
        form = ShippingForm()

    return render(request, 'billing/shipping.html', {'form': form, 'item': item})

@login_required
def payment(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    amount = item.sale_price if item.is_sale else item.price
    amount_in_cents = int(amount * 100)  # Stripe expects the amount in cents

    if request.method == 'POST':
        token = request.POST['stripeToken']
        try:
            charge = stripe.Charge.create(
                amount=amount_in_cents,  # Amount in cents
                currency='gbp',  # Adjust currency if necessary
                description=f'Charge for {item.name}',
                source=token,
            )

            # Store item_id in session to retrieve it in the payment_success view
            request.session['item_id'] = item_id

            return redirect('billing:payment_success')
        except stripe.error.CardError as e:
            body = e.json_body
            err = body['error']
            return render(request, 'billing/payment.html', {'error': err['message'], 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'item': item})
        except stripe.error.StripeError as e:
            return render(request, 'billing/payment.html', {'error': 'Something went wrong. You were not charged. Please try again.', 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'item': item})

    return render(request, 'billing/payment.html', {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'item': item, 'amount': amount_in_cents})

@login_required
def payment_success(request):
    try:
        # Get the shipping details for the current user
        shipping_details = ShippingAddress.objects.filter(user=request.user).latest('id')

        # Get the item ID from the session
        item_id = request.session.get('item_id')
        item = Item.objects.get(pk=item_id)

        # Determine the user for the order
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        # Create an order with billing information and item details
        order = Order.objects.create(
            item=item,
            user=user,
            quantity=1,  # Assuming you're ordering one item at a time
            address=shipping_details.shipping_address,
            phone=shipping_details.shipping_phone,
            full_name=shipping_details.shipping_fullname,
            email=shipping_details.shipping_email,
            city=shipping_details.city,
            country=shipping_details.shipping_country,
            post_code=shipping_details.shipping_postcode,
            date=timezone.now(),
            status=True,  # Set to True assuming it's paid
        )

        # Clear the session variable
        del request.session['item_id']

        return render(request, 'billing/payment_success.html', {'order': order})
    except Exception as e:
        print("Error:", str(e))  # Debug statement
        return render(request, 'billing/payment_success.html', {'error': 'Something went wrong. Please try again.'})