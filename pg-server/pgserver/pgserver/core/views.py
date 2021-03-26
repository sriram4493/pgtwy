import paypal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from . import Checksum
from .utils import VerifyPaytmResponse
from .models import Transaction,UserProfile
from datetime import datetime,timezone as tz
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

@api_view(["GET"])
def get_transactions(request):
    """
    :param request:
    :return: List of transactions based on user Transactions
    """
    try:
        user = request.user
        user_id = User.objects.get(username=user)
        print(user_id)
        transactions = Transaction.objects.filter(user_id__user=user_id).values('status','amount','to_account','date','payment_method')
        print(transactions)
        return Response({"transactions":transactions})
    except Exception as e:
        print(e)
        return Response("Could Not List the Transactions".format(str(e)), status=HTTP_400_BAD_REQUEST)

def payment(request):
    order_id = Checksum.__id_generator__()
    amount = "1"
    user = str(request.user)
    user_object = UserProfile.objects.filter(user__username=user).values('phone_number',email = F('user__email'))
    email = user_object[0]['email']
    phone_number = user_object[0]['phone_number']
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': str(phone_number),
        'EMAIL': email,
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': amount,
    }
    data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    user_profile_object = UserProfile.objects.get(user__username=user)
    # Initiate Transaction
    Transaction.objects.get_or_create(user_id = user_profile_object,id =order_id)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'paytm.html', context)



@csrf_exempt
@api_view(["POST"])
def paytm_response(request):
    """
    Paytm call back url to save the transaction Details
    """
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        response = resp['paytm']
        try:
            txn_object = Transaction.objects.get(id=response['ORDERID'])
            txn_object.txn_id=response['TXNID']
            txn_object.amount=response['TXNAMOUNT']
            txn_object.status=response['STATUS']
            txn_object.payment_method='paytm'
            txn_object.date = str(datetime.now(tz.utc))
            txn_object.save()
            return HttpResponse({"message": "Transaction Sucessful"}, status=200)
        except ObjectDoesNotExist as e:
            return HttpResponse({"message":"Transaction Was Not Initiated"}, status=200)
    else:
        return HttpResponse({"message":"Transaction Failed"}, status=400)

def process_payment(request):
    order = Checksum.__id_generator__()
    # order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '',
        'item_name': 'Order {}'.format(order),
        'invoice': str(order),
        'currency_code': 'INR',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'paypal.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request):
    return render(request, 'paypal_sucess.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'paypal_failure.html')