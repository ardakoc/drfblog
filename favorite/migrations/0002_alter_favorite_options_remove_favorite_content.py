# Generated by Django 4.1.7 on 2023-03-16 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorite', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='content',
        ),
    ]
