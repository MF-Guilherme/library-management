# Generated by Django 5.1.2 on 2024-10-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_synopsis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='synopsis',
            field=models.TextField(blank=True, null=True),
        ),
    ]
