from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from core.models import Product, OrderDetail
import json
import stripe
import logging

# setup logger
logger = logging.getLogger(__name__)

class IndexView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = "index.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        return context


@csrf_exempt
def stripe_checkout_session(request, pk):
    request_data = json.loads(request.body)  # parse valid json string to python dict
    product = get_object_or_404(Product, pk=pk)

    # get quantity from request, default to 1 if not provided
    quantity = int(request_data.get("quantity", 1))

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                "price_data": {
                    "currency": "pkr",
                    "product_data": {
                        "name": product.name,
                        "description": product.body,
                    },
                    "unit_amount": int(product.price * 100),
                },
                "quantity": quantity,
            }
        ],
        mode="payment",
        customer_creation='always',
        success_url="https://864tlzrs-8000.inc1.devtunnels.ms/success/?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=settings.PAYMENT_CANCEL_URL,
          
    )

    # total amount = price * quantity
    total_amount = int(product.price * 100) * quantity

    order = OrderDetail.objects.create(
        customer_email=request_data['email'],
        product=product,
        stripe_id=checkout_session['id'],
        quantity=quantity,
        amount=total_amount,
    )
    order.save()

    return JsonResponse({
        "sessionId": checkout_session.id
    })

@csrf_exempt
def stripe_webhook(request):
    # ✅ Print all incoming request info
    print("⚡ New webhook request received")
    print("Method:", request.method)
    print("Headers:", dict(request.headers))
    try:
        print("Body:", request.body.decode('utf-8'))
    except UnicodeDecodeError:
        print("Body: (binary content)")

    payload = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    event = None

    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if sig_header:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            print("⚠️ Invalid payload")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            print("⚠️ Invalid signature")
            return HttpResponse(status=400)
    else:
        try:
            event = json.loads(payload)
        except Exception:
            print("⚠️ Cannot parse webhook body")
            return HttpResponse(status=400)

    print(f"📩 Webhook event type: {event.get('type')}")

    # Handle checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"✅ Checkout completed for session ID: {session.get('id')}")

        order = OrderDetail.objects.filter(stripe_id=session.get("id")).first()
        if order:
            metadata = {
                "product_id": str(order.product.id),
                "product_name": order.product.name,
                "customer_email": order.customer_email if hasattr(order, "customer_email") else session.get("customer_email"),
                "order_id": str(order.id),
                "extra_info": "Ibtisam Ul Haq",
                "status": "Paid" if order.has_paid else "Pending"
            }

            print("🔹 Metadata (from webhook/db):")
            for key, value in metadata.items():
                print(f"   • {key}: {value}")

        # ✅ Show customer email
        print(f"👤 Customer email: {session.get('customer_email')}")

        # ✅ Mark order as paid
        order = OrderDetail.objects.filter(stripe_id=session.get("id")).first()
        if order:
            order.has_paid = True
            order.save()
            print(f"💾 Order {order.id} marked as paid")
        else:
            print("⚠️ Order not found for this session ID")

    return HttpResponse(status=200)

class SuccessView(TemplateView):
    template_name = "payment/success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        # ✅ fixed here: use session.id instead of session.stripe_id
        order = get_object_or_404(OrderDetail, stripe_id=session.id)
        order.has_paid = True
        order.save()

        return render(request, self.template_name)


class CancelView(TemplateView):
    template_name = "payment/cancel.html"


class OrderHistroyView(ListView):
    model = OrderDetail
    context_object_name = 'orders'
    template_name = 'product/order_histroy.html'
