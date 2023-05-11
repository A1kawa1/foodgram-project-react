# Generated by Django 3.2.16 on 2023-05-11 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230511_1619'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='Проверка уникальности подписки',
        ),
        migrations.RemoveConstraint(
            model_name='follow',
            name='Проверка подписки на самого себя',
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user', 'author')},
        ),
    ]