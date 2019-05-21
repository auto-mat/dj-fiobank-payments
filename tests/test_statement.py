# -*- coding: utf-8 -*-

# Author: Petr Dlouhý <petr.dlouhy@auto-mat.cz>
#
# Copyright (C) 2016 o.s. Auto*Mat
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
from unittest.mock import MagicMock, patch

from dj_fiobank_payments.models import Payment
from dj_fiobank_payments.statement import parse

from django.test import TestCase

from model_mommy import mommy

from .models import Order


class TestPasswordForms(TestCase):
    @patch('fiobank.FioBank')
    def test_parse_match(self, fiobank):
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123,
                'variable_symbol': '000112233',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'CZK',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': 'message',
                'user_identification': 'Foo User',
            },
        ]
        parse()
        order.refresh_from_db()
        self.assertEqual(order.paid_date, datetime.date(2017, 1, 1))

    @patch('fiobank.FioBank')
    def test_parse_match_ammount_difference(self, fiobank):
        """ Test math if the ammount is within 1 CZK margin """
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123.9,
                'variable_symbol': '000112233',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'CZK',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': 'message',
                'user_identification': 'Foo User',
            },
        ]
        parse()
        order.refresh_from_db()
        self.assertEqual(order.paid_date, datetime.date(2017, 1, 1))

    @patch('builtins.print', autospec=True, side_effect=print)
    @patch('fiobank.FioBank')
    def test_parse_no_match_ammount_difference(self, fiobank, mock_logger):
        """ Test no math if the ammount is out of 1 CZK margin """
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        for ammount in (121.9, 124.1):
            m.period.return_value = [
                {
                    'amount': ammount,
                    'variable_symbol': '000112233',
                    'specific_symbol': '124',
                    'account_number_full': '125',
                    'constant_symbol': '126',
                    'instruction_id': '127',
                    'transaction_id': '128',
                    'comment': '129',
                    'bank_name': '130',
                    'account_number': '130',
                    'currency': 'CZK',
                    'bank_code': '234234',
                    'type': 'type',
                    'account_name': 'type',
                    'date': '2017-01-01',
                    'recipient_message': 'message',
                    'user_identification': 'Foo User',
                },
            ]
            parse()
            mock_logger.assert_called_with(
                "'124', '125', 'type', '000112233', '%s', 'message', 'type', '2017-01-01', "
                "'126', '127', '128', '129', '130', '130', 'CZK', '234234', 'Foo User'" % ammount,
            )

    @patch('fiobank.FioBank')
    def test_parse_match_recipient_message(self, fiobank):
        """ Test, that it matches also if variable symbol is in recipient message """
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123,
                'variable_symbol': '',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'CZK',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': 'D00112/233',
                'user_identification': 'Foo User',
            },
        ]
        parse()
        order.refresh_from_db()
        self.assertEqual(order.paid_date, datetime.date(2017, 1, 1))

    @patch('fiobank.FioBank')
    def test_parse_match_no_recipient_message(self, fiobank):
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123,
                'variable_symbol': '112233',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'CZK',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': None,
                'user_identification': 'Foo User',
            },
        ]
        parse()
        order.refresh_from_db()
        payment = Payment.objects.get()
        self.assertEqual(order.paid_date, datetime.date(2017, 1, 1))
        self.assertEqual(payment.order, order)
        self.assertEquals(payment.amount, '123')

    @patch('builtins.print', autospec=True, side_effect=print)
    @patch('fiobank.FioBank')
    def test_parse_no_match(self, fiobank, mock_logger):
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123,
                'variable_symbol': '112233',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'CZK',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': 'message',
                'user_identification': 'Foo User',
            },
        ]
        parse()
        mock_logger.assert_called_with(
            "'124', '125', 'type', '112233', '123', 'message', 'type', '2017-01-01', "
            "'126', '127', '128', '129', '130', '130', 'CZK', '234234', 'Foo User'",
        )
        payment = Payment.objects.get()
        self.assertEquals(payment.amount, '123')

    @patch('builtins.print', autospec=True, side_effect=print)
    @patch('fiobank.FioBank')
    def test_parse_no_czk(self, fiobank, mock_logger):
        order = mommy.make("Order", variable_symbol="112233")
        order.total_amount = 123
        order.save()
        m = MagicMock()
        fiobank.return_value = m
        m.period.return_value = [
            {
                'amount': 123,
                'variable_symbol': '112233',
                'specific_symbol': '124',
                'account_number_full': '125',
                'constant_symbol': '126',
                'instruction_id': '127',
                'transaction_id': '128',
                'comment': '129',
                'bank_name': '130',
                'account_number': '130',
                'currency': 'USD',
                'bank_code': '234234',
                'type': 'type',
                'account_name': 'type',
                'date': '2017-01-01',
                'recipient_message': 'message',
                'user_identification': 'Foo User',
            },
        ]
        parse()
        mock_logger.assert_called_with(
            "'124', '125', 'type', '112233', '123', 'message', 'type', '2017-01-01', "
            "'126', '127', '128', '129', '130', '130', 'USD', '234234', 'Foo User'",
        )
        payment = Payment.objects.get()
        self.assertEquals(payment.amount, '123')
