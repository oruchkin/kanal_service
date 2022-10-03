from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Order, Telegram_notification
from .utils import (check_delivery_time_expiration, get_data_from_google_sheet,
                    get_dollar_value, send_notification_teleg)


def index(request):
    """
    Вывод графика и таблицы с заказами, данные беруться из базы данных.
    """
    all_orders = Order.objects.all().order_by('number')
    try:
        max_usd_value = all_orders.order_by('-price_usd')[0].price_usd
        min_usd_value = all_orders.order_by('price_usd')[0].price_usd
    except:
        max_usd_value = 0
        min_usd_value = 0
    x_values = []
    y_values = []
    total_sum = 0
    #находим данные для отображения графика
    for order in all_orders:
        y_values.append(order.price_usd) 
        x_values.append(order.number)
        total_sum += order.price_usd

    context = {"rub":get_dollar_value(),
               "all_orders":Order.objects.all().order_by('pk'),
               "x_values":x_values,
               "y_values":y_values,
               "max_usd_value":max_usd_value,
               "min_usd_value":min_usd_value,
               "total_sum":total_sum}
    return render(request, 'sheets/index.html', context)    


def data_recieving(request):
    """
    Получение данных из google sheet, и обновление(сохранение) их в базе данных.
    """
    data = get_data_from_google_sheet()
    usd_value = get_dollar_value()
    info = data[1:]
    Order.objects.all().delete()
    all_admins = Telegram_notification.objects.all()
    count = 2
    message_about_expiration = ""
    for order in info:
        #удостоверяемся что даные строчки в необходимом формате
        try:
            price_usd = float(order[2])
            price_rub = round(price_usd * usd_value,2)
            new_order = Order(number = order[0],order_number = order[1],
                            delivery_time = datetime.strptime(order[3], '%d.%m.%Y'),
                            price_usd = price_usd, price_rub = price_rub)
            check_expiration = check_delivery_time_expiration(new_order)
            if check_expiration:
                message_about_expiration += f"заказ номер {new_order.order_number} - просрочен! \n"
            new_order.save()
            count += 1
        #если формат не верный,строчку не сохраняем и отправляем уведомление об ошибке
        except: 
            for admin in all_admins:
                text_message = f"строка {count} заполнена не коректно"
                send_notification_teleg(admin.chat_id, text_message)
            count += 1
            continue
    # рассылка уведомлений о просроченых доставках
    if message_about_expiration:
        for admin in all_admins:
            send_notification_teleg(admin.chat_id, message_about_expiration)
    return HttpResponseRedirect(reverse('index'))