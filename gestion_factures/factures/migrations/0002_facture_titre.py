# Generated by Django 5.1.2 on 2024-10-22 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='titre',
            field=models.CharField(default='Titre manquant', max_length=200),
            preserve_default=False,
        ),
    ]