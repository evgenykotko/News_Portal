# Generated by Django 4.0.2 on 2022-03-17 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsportal', '0004_alter_category_subscribers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category_post',
        ),
        migrations.AddField(
            model_name='post',
            name='category_post',
            field=models.ManyToManyField(to='newsportal.Category'),
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]
