# Generated by Django 3.2.16 on 2023-05-10 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(unique=True, verbose_name='Описание'),
        ),
    ]
