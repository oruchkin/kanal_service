from django.contrib import admin

from .models import Order, Telegram_notification


@admin.register(Order)
class Order_Admin(admin.ModelAdmin):
    list_display = ['number', 'order_number', 'delivery_time', 'price_usd', 'price_rub']
    search_fields = ['order_number']


@admin.register(Telegram_notification)
class Telegram_notification_Admin(admin.ModelAdmin):
    list_display = ['name', 'chat_id']
    search_fields = ['name', 'chat_id']