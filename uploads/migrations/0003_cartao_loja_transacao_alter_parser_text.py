# Generated by Django 4.0.1 on 2022-01-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_alter_parser_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Loja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(default='', max_length=11)),
                ('nome', models.CharField(default='', max_length=19)),
                ('representante', models.CharField(default='', max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField()),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='parser',
            name='text',
            field=models.TextField(default=None),
        ),
    ]
