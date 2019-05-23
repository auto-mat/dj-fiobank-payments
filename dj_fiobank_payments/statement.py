# -*- coding: utf-8 -*-
# Author: Petr Dlouhý <petr.dlouhy@email.cz>
#
# Copyright (C) 2017 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import datetime
import logging
import re

import django
from django.conf import settings

import fiobank

from .models import FioPayment
Order = django.apps.apps.get_model(*settings.FIOBANK_PAYMENTS_ORDER_MODEL.split('.', 1))

logger = logging.getLogger(__name__)


columns = [
    'specific_symbol',
    'account_number_full',
    'type',
    'variable_symbol',
    'amount',
    'recipient_message',
    'account_name',
    'date',
    'constant_symbol',
    'instruction_id',
    'transaction_id',
    'comment',
    'bank_name',
    'account_number',
    'currency',
    'bank_code',
    'user_identification',
]


def parse(days_back=7):
    client = fiobank.FioBank(token=settings.FIO_TOKEN)
    gen = client.period(
        datetime.datetime.now() - datetime.timedelta(days=days_back),
        datetime.datetime.now(),
    )
    for payment in gen:
        if payment['amount'] >= 0:
            variable_symbol = payment['variable_symbol']
            recipient_message = payment['recipient_message']
            if recipient_message:
                # Replace all non-letter characters and leading zeros from VS
                recipient_message_without_d = re.sub("\D", "", recipient_message).lstrip("0") # noqa
            else:
                recipient_message_without_d = ""
            if variable_symbol:
                variable_symbol = variable_symbol.lstrip("0")
            else:
                variable_symbol = ""

            try:
                order = Order.objects.get(
                    variable_symbol__in=(variable_symbol, recipient_message, recipient_message_without_d),
                    total_amount__lte=payment['amount'] + 1,
                    total_amount__gte=payment['amount'] - 1,
                )
                if 'CZK' == payment['currency']:
                    order.paid_date = payment['date']
                    order.save()
            except Order.DoesNotExist:
                order = None
            new_payment, created = FioPayment.objects.get_or_create(
                ident=payment['transaction_id'],
                defaults={
                    'message': payment['recipient_message'],
                    'symspc': payment['specific_symbol'],
                    'symvar': variable_symbol,
                    'currency': payment['currency'],
                    'amount': payment['amount'],
                    'received_at': payment['date'],
                    'user_identification': payment['user_identification'],
                    'bank': payment['bank_name'],
                    'symcon': payment['constant_symbol'],
                    'sender': payment['account_number'],
                    'status': 'paid',
                },
            )
            new_payment.order = order
            new_payment.save()
