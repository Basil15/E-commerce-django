# Generated by Django 3.2.19 on 2023-06-21 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_app', '0002_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('update_desc', models.CharField(max_length=5000)),
            ],
        ),
    ]