# Generated by Django 3.1.7 on 2021-03-25 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField()),
                ('address', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('status', models.TextField(max_length=15)),
                ('amount', models.FloatField()),
                ('to_account', models.TextField()),
                ('payment_method', models.CharField(choices=[('paytm', 'paytm'), ('paypal', 'paypal')], max_length=15)),
                ('date', models.DateTimeField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.userprofile')),
            ],
        ),
    ]
