from django.db import models

class Time_Stamped_Mixin(models.Model):
    """
    Абстрактный класс с полями времени.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Order(Time_Stamped_Mixin):
    """
    Таблица для заказов.
    """
    number = models.IntegerField()
    order_number =  models.IntegerField()
    delivery_time = models.DateField()
    price_usd  = models.FloatField()
    price_rub = models.FloatField()    
    def __str__(self):
        return f"{self.number}"


class Telegram_notification(Time_Stamped_Mixin):
    """
    Модель для ввода администраторов, которым будут разосланы 
    уведомления в телеграмме.
    """
    name = models.CharField(max_length = 150)
    chat_id = models.CharField(max_length = 150)
    def __str__(self):
        return self.name
