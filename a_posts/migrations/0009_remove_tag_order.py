# Generated by Django 4.2 on 2023-05-31 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0008_tag_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='order',
        ),
    ]
