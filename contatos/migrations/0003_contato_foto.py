# Generated by Django 4.0.4 on 2022-04-24 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0002_contato_mostrar'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='foto',
            field=models.ImageField(blank=True, upload_to='foto/%Y/%m/%d'),
        ),
    ]