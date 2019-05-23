
from django.contrib import admin

from .models import FioPayment


@admin.register(FioPayment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin model for Payments."""
    list_display = (
        'ident',
        'order',
        'user_identification',
        'symvar',
        'symcon',
        'symspc',
        'amount',
        'sender',
        'bank',
        'message',
        'currency',
        'received_at',
    )
    list_filter = ('bank',)

    def get_readonly_fields(self, request, obj=None):
        """Define all read only fields."""
        if obj:
            return [
                'ident',
                'symvar',
                'symcon',
                'symspc',
                'amount',
                'sender',
                'bank',
                'message',
                'currency',
                'received_at',
            ]
        return super(PaymentAdmin, self).get_readonly_fields(
            request,
            obj,
        )
