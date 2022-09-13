# Generated by Django 3.2.8 on 2022-07-18 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quitance', '0004_auto_20220717_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartiVersante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom', models.CharField(max_length=200, verbose_name='Nom et Prénom')),
                ('reference', models.CharField(max_length=50, verbose_name='Nif/Matricule')),
                ('adresse', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse')),
                ('telephone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse')),
                ('mail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Adresse')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TypePartiVersante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libele', models.CharField(max_length=100, verbose_name='Libele')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quitance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.BigIntegerField(verbose_name='Montant')),
                ('nature', models.CharField(max_length=200, verbose_name='Nature')),
                ('nom_prenom', models.CharField(max_length=100, verbose_name='Nom et Prénom')),
                ('nom_partie_versante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom Parti Versante')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bordereau', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quitance.bordereau')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('partie_versante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quitance.partiversante')),
            ],
        ),
        migrations.AddField(
            model_name='partiversante',
            name='type_versante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quitance.typepartiversante'),
        ),
    ]
