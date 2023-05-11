# Generated by Django 3.2.16 on 2023-05-11 13:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_alter_recipe_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(flags=0, message='Недопустимый цвет (только нижний регистр)', regex='^#[a-f0-9]{6}$')], verbose_name='Цвет'),
        ),
    ]
