from __future__ import absolute_import, unicode_literals
from .models import Card, CardPriceHistory, CardPriceNotification, CardPriceNotificationMessage
from .views import get_access_token
from celery import app as celery_app
import requests
import json
import datetime


@celery_app.shared_task
def record_current_price():
    access_token = get_access_token()

    card_qs = Card.objects.all()

    for card in card_qs:
        search_url = f'https://api.tcgplayer.com/pricing/product/{card.product_ID}'
        headers = {'Authorization': f'Bearer {access_token}'}
        res = requests.get(search_url, headers=headers)

        results = res.json()['results']

        # Records card's today price
        results_json = json.dumps(results)
        # filter out card editions with no market price
        input_dict = json.loads(results_json)
        output_dict = [x for x in input_dict if x['marketPrice'] != None]

        if len(output_dict) > 0:
            card.latest_price = output_dict[0]['marketPrice']
            card.latest_price_card_type = output_dict[0]['subTypeName']
            card.save()

            # A price check needs to happen for each card editions of the same card
            for edition in output_dict:
                card_edition = edition['subTypeName']
                current_price = edition['marketPrice']

                # Get all the notification settings set for the current card edition
                notification_setting_qs = CardPriceNotification.objects.filter(
                    card=card, card_edition=card_edition)

                for notification in notification_setting_qs:
                    if notification.above_price < current_price:
                        above_notification = CardPriceNotificationMessage(user=notification.user, card_name=card.card_name, card_edition=card_edition,
                                                                          notification_type='A', threshold_price=notification.above_price, current_price=current_price)
                        above_notification.save()

                    if notification.below_price > current_price:
                        below_notification = CardPriceNotificationMessage(user=notification.user, card_name=card.card_name, card_edition=card_edition,
                                                                          notification_type='B', threshold_price=notification.below_price, current_price=current_price)
                        below_notification.save()

            output_json = json.dumps(output_dict)
            # prices field converts 'output_dict' to json
            card_price_history = CardPriceHistory(
                card=card, date=datetime.date.today(), prices=output_json)

            if card_price_history:
                card_price_history.save()


# @celery_app.shared_task
# def send_price_notifications():
