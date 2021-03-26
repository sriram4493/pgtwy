from django.urls import path,include
from .views import get_transactions,payment,paytm_response,process_payment,payment_done,payment_canceled

urlpatterns = [
    path("transactions/",get_transactions,name='get_transactions'),
    path("pay/paytm/",payment,name='pay_paytm'),
    path("paytm/response/",paytm_response, name='paytm_response'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment-done/', payment_done, name='payment_done'),
    path('payment-cancelled/', payment_canceled, name='payment_cancelled'),
]