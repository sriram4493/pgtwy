from django.urls import path,include
from .views import get_transactions,payment,paytm_response

urlpatterns = [
    path("transactions/",get_transactions),
    path("pay/paytm/",payment),
    path("paytm/response/",paytm_response)
    # path("pay/paypal/"),
    # path("pay/razorpay/")
]