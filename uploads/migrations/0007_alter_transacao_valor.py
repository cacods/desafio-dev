# Generated by Django 4.0.1 on 2022-01-26 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0006_alter_transacao_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacao',
            name='valor',
            field=models.FloatField(default=None),
        ),
    ]
