# Generated by Django 4.2.16 on 2024-11-25 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_category_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='embeddign',
            new_name='embedding',
        ),
    ]
