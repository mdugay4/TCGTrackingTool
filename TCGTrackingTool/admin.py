from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Card, Inventory, CardPriceHistory, CardPriceNotification, CardPriceNotificationMessage


class CardAdmin(admin.ModelAdmin):

    list_display = ('card_name', 'product_ID',
                    'image_url', 'category_ID', 'group_ID')

    search_fields = ('card_name', 'product_ID')


admin.site.register(Card, CardAdmin)


class CardPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('card', 'date')
    search_fields = ('card', 'date')


admin.site.register(CardPriceHistory, CardPriceHistoryAdmin)


class CardPriceNotificationAdmin(admin.ModelAdmin):
    list_display = ('card', 'product_ID', 'user', 'below_price', 'above_price')
    search_fields = ('card', 'user')


admin.site.register(CardPriceNotification, CardPriceNotificationAdmin)


class CardPriceNotificationMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_name', 'card_edition',
                    'notification_type', 'threshold_price', 'current_price')


admin.site.register(CardPriceNotificationMessage,
                    CardPriceNotificationMessageAdmin)
