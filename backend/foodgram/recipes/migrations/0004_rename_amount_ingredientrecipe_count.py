# Generated by Django 4.2.1 on 2023-05-03 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_hex_tag_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientrecipe',
            old_name='amount',
            new_name='count',
        ),
    ]
