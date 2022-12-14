# Generated by Django 4.1.1 on 2022-10-10 21:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_comments_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='startingBid',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listings',
            name='bid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.bids'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='auctions.categories'),
        ),
    ]
