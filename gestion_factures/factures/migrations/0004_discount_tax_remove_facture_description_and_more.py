# Generated by Django 5.1.2 on 2024-10-24 12:15

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factures', '0003_client_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
        ),
        migrations.RemoveField(
            model_name='facture',
            name='description',
        ),
        migrations.AddField(
            model_name='client',
            name='country',
            field=django_countries.fields.CountryField(default='FR', max_length=2),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='factures.facture')),
            ],
        ),
        migrations.AddField(
            model_name='facture',
            name='discounts',
            field=models.ManyToManyField(blank=True, to='factures.discount'),
        ),
    ]
