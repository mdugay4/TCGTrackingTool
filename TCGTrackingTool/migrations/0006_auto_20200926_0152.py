# Generated by Django 3.1.1 on 2020-09-26 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TCGTrackingTool', '0005_cardpricehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpricehistory',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='TCGTrackingTool.card'),
        ),
    ]
