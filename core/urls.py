from django.urls import path
from core import views
app_name = "core"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('orders/histroy', views.OrderHistroyView.as_view(), name='order_histroy'),
    path('<int:pk>/detail/', views.ProductDetailView.as_view(), name='detail'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('checkout_session/<int:pk>/', views.stripe_checkout_session, name="stripe_checkout_session"),
]