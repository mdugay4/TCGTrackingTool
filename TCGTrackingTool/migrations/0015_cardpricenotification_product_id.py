# Generated by Django 3.1.1 on 2020-12-03 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCGTrackingTool', '0014_auto_20201128_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpricenotification',
            name='product_ID',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
