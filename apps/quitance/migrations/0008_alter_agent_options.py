# Generated by Django 3.2.8 on 2022-07-19 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quitance', '0007_auto_20220719_1935'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'permissions': (('versement_numeraire', 'Peut effectuer un versement numeraire'), ('depot_cheque', 'Peut effectuer un dépôt chèque'), ('reprint_quitance', 'Peut reimprimer une quitance')), 'verbose_name': 'Agent', 'verbose_name_plural': 'Agents'},
        ),
    ]