# Generated by Django 4.2.3 on 2023-07-09 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0003_alter_conta_banco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='banco',
            field=models.CharField(choices=[('BB', 'Banco do Brasil'), ('CE', 'Caixa econômica'), ('NU', 'Nubank')], max_length=2),
        ),
    ]
