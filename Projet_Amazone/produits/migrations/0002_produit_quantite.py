# Generated by Django 5.0.6 on 2024-07-15 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='quantite',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
