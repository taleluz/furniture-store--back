from celery import shared_task
from django.utils import timezone
from .models import Order


@shared_task
def update_order_status():
    orders = Order.objects.filter(isDelivered=False, deliveredAt__lte=timezone.now())
    for order in orders:
        order.isDelivered = True
        order.save()