# Generated by Django 3.2.8 on 2022-07-16 17:39

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bordereau',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=10, verbose_name='Numero du bordereau')),
                ('type_operation', models.IntegerField(choices=[(1, 'DEPOT CHEQUE'), (2, 'VERSEMENT NUMERAIRE')], verbose_name='Type Operation')),
                ('date', models.DateField(verbose_name='Date du bordereau')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Bordereau',
                'verbose_name_plural': 'Bordereaux',
            },
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpt', models.CharField(max_length=15, unique=True, verbose_name='Compte')),
                ('libele', models.CharField(max_length=100, unique=True, verbose_name='Intitulé du compte')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Compte',
                'verbose_name_plural': 'Comptes',
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libele', models.CharField(max_length=100, unique=True, verbose_name='Poste comptable')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Code')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Structure',
                'verbose_name_plural': 'Structures',
            },
        ),
        migrations.CreateModel(
            name='SousStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libele', models.CharField(max_length=100, verbose_name='Poste comptable')),
                ('numero', models.CharField(max_length=10, unique=True, verbose_name='Numéro poste')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quitance.structure')),
            ],
            options={
                'verbose_name': 'Sous Structure',
                'verbose_name_plural': 'Sous Structures',
                'unique_together': {('libele', 'structure')},
            },
        ),
        migrations.CreateModel(
            name='BordereauDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ischeque', models.BooleanField(verbose_name='Is cheque')),
                ('montant', models.BigIntegerField(verbose_name='Montant')),
                ('nature', models.CharField(max_length=200, verbose_name='Nature')),
                ('partie_versante', models.CharField(max_length=100, verbose_name='Partie versante')),
                ('num_cheque', models.CharField(blank=True, max_length=10, null=True, verbose_name='Numero du cheque')),
                ('banque', models.CharField(blank=True, max_length=50, null=True, verbose_name='Banque du cheque')),
                ('date_cheque', models.DateField(blank=True, null=True, verbose_name='Date du cheque')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bordereau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quitance.bordereau')),
            ],
            options={
                'verbose_name': 'Détails Bordereau',
                'verbose_name_plural': 'Détails Bordereaux',
            },
        ),
        migrations.AddField(
            model_name='bordereau',
            name='compte',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quitance.compte'),
        ),
        migrations.AddField(
            model_name='bordereau',
            name='poste_comptable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quitance.sousstructure'),
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cgib', models.CharField(blank=True, max_length=50, null=True, verbose_name='CGIB compte')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Agent',
                'verbose_name_plural': 'Agents',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
