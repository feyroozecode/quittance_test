# Generated by Django 3.2.8 on 2022-07-19 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quitance', '0009_auto_20220719_2214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journee',
            options={'verbose_name': 'Journee', 'verbose_name_plural': 'Journees'},
        ),
        migrations.RemoveField(
            model_name='bordereaudetail',
            name='partie_versante',
        ),
    ]