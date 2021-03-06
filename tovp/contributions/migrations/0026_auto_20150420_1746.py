# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contributions', '0025_auto_20150416_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkpayment',
            name='payment_method',
            field=models.CharField(verbose_name='Payment Method', max_length=16, choices=[('cashl', 'Cash (Indian)'), ('cashf', 'Cash (Foreign)'), ('cashd', 'Cash Deposit'), ('ccdcsl', 'Credit/Debit Card Swipe Local'), ('ccdcsf', 'Credit/Debit Card Swipe Foreign'), ('neftl', 'NEFT (Indian)'), ('neftf', 'NEFT (Foreign)'), ('chequel', 'Cheque (Indian)'), ('chequef', 'Cheque (Foreign)'), ('chequed', 'Cheque Deposit'), ('paypal', 'Paypal'), ('axis', 'Gateway Axis (Internet)'), ('treasury', 'ISKCON Treasury'), ('bulk', 'Part of the Bulk Payment')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contribution',
            name='payment_method',
            field=models.CharField(verbose_name='Payment Method', max_length=16, choices=[('cashl', 'Cash (Indian)'), ('cashf', 'Cash (Foreign)'), ('cashd', 'Cash Deposit'), ('ccdcsl', 'Credit/Debit Card Swipe Local'), ('ccdcsf', 'Credit/Debit Card Swipe Foreign'), ('neftl', 'NEFT (Indian)'), ('neftf', 'NEFT (Foreign)'), ('chequel', 'Cheque (Indian)'), ('chequef', 'Cheque (Foreign)'), ('chequed', 'Cheque Deposit'), ('paypal', 'Paypal'), ('axis', 'Gateway Axis (Internet)'), ('treasury', 'ISKCON Treasury'), ('bulk', 'Part of the Bulk Payment')]),
            preserve_default=True,
        ),
    ]
