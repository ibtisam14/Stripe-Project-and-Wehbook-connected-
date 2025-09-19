from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
from core.models import Product, OrderDetail
import json
import stripe

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
                "quantity": quantity,   # <-- now dynamic
            }
        ],
        mode="payment",
        customer_creation='always',
        success_url=settings.PAYMENT_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
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

class SuccessView(TemplateView):
    template_name = "payment/success.html"
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        stripe.api_key = settings.STRIPE_PRIVATE_KEY
        session = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(OrderDetail, stripe_id=session.stripe_id)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class CancelView(TemplateView):
    template_name = "payment/cancel.html"


class OrderHistroyView(ListView):
    model = OrderDetail
    context_object_name = 'orders'
    template_name = 'product/order_histroy.html'
