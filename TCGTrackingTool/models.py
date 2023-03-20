# Custom User Model
from django.db import models
from django.contrib.auth.models import User


# Card & Inventory Models
class Card(models.Model):
    inventory = models.ManyToManyField("Inventory")

    product_ID = models.IntegerField()
    card_name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    category_ID = models.IntegerField()
    group_ID = models.IntegerField()
    url = models.CharField(max_length=100)

    latest_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    latest_price_card_type = models.CharField(
        max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.card_name}: {self.product_ID}'


class CardPriceHistory(models.Model):
    '''
    Represents a card's price at a single date
    '''
    card = models.ForeignKey(
        'Card', related_name='history', on_delete=models.CASCADE)
    date = models.DateField()
    prices = models.CharField(max_length=500)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return f'{self.card}: {self.prices}'


class Inventory(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)


class CardPriceNotification(models.Model):
    card = models.ForeignKey(
        'Card', related_name='notification', on_delete=models.CASCADE)

    card_name = models.CharField(max_length=60)
    product_ID = models.IntegerField()
    card_edition = models.CharField(max_length=60)
    below_price = models.DecimalField(max_digits=6, decimal_places=2)
    above_price = models.DecimalField(max_digits=6, decimal_places=2)

    user = models.ForeignKey(
        User, related_name='notification', on_delete=models.CASCADE)


class CardPriceNotificationMessage(models.Model):

    NOTIFICATION_TYPE = (
        ('B', 'Below Notification'),
        ('A', 'Above Notification')
    )

    user = models.ForeignKey(
        User, related_name='notification_message', on_delete=models.CASCADE)
    card_name = models.CharField(max_length=60)
    card_edition = models.CharField(max_length=60)
    notification_type = models.CharField(
        max_length=1, choices=NOTIFICATION_TYPE)
    threshold_price = models.DecimalField(max_digits=5, decimal_places=2)
    current_price = models.DecimalField(max_digits=5, decimal_places=2)
