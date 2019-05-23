
from django.contrib import admin

from .models import FioPayment


@admin.register(FioPayment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin model for Payments."""
    list_display = (
        'ident',
        'order',
        'user_identification',
        'status',
        'symvar',
        'symcon',
        'symspc',
        'amount',
        'sender',
        'bank',
        'message',
        'currency',
        'received_at',
        'note',
    )
    list_filter = (
        'bank',
        'order',
        'status',
    )
    list_editable = (
        'note',
    )
    search_fields = (
        'ident',
        'order__id',
        'user_identification',
        'status',
        'symvar',
        'symcon',
        'symspc',
        'amount',
        'sender',
        'bank',
        'message',
        'currency',
        'received_at',
        'note',
    )

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
