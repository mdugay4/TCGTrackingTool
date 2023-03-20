from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Card, CardPriceHistory, CardPriceNotification, CardPriceNotificationMessage

# -----------------------------------------------------
# * Card Serializer


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ['product_ID', 'card_name',
                  'image_url', 'category_ID', 'group_ID', 'url', 'latest_price', 'latest_price_card_type']


class CardPriceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CardPriceHistory
        fields = ['card', 'date', 'prices']


class SendCardInventorySerializer(serializers.ModelSerializer):

    productId = serializers.CharField(source='product_ID')
    name = serializers.CharField(source='card_name')
    imageUrl = serializers.CharField(source='image_url')
    categoryId = serializers.CharField(source='category_ID')
    groupId = serializers.CharField(source='group_ID')

    class Meta:
        model = Card
        fields = ['productId', 'name',
                  'imageUrl', 'categoryId', 'groupId']


class CardPriceNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardPriceNotification
        fields = ('card', 'product_ID', 'card_name', 'card_edition',
                  'user', 'below_price', 'above_price')


class CardPriceNotificationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardPriceNotificationMessage
        fields = ('user', 'card_name', 'card_edition',
                  'notification_type', 'threshold_price', 'current_price')
