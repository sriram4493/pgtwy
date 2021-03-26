from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    address = models.TextField()


class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('paytm', 'paytm'),
        ('paypal', 'paypal')
    )
    user_id = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING)
    id = models.TextField(null=False, primary_key=True)
    txn_id = models.TextField(null=True)
    status = models.TextField(max_length=15,null=True)
    amount = models.FloatField(null=True)
    to_account = models.TextField(null=True)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, null=True)
    date = models.DateTimeField(null=True)
