# Generated by Django 3.1.7 on 2022-03-24 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0045_auto_20220324_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batdata',
            name='x_113_Estimate_microli_x',
            field=models.TextField(null=True, verbose_name='Estimate microliters of blood drawn'),
        ),
    ]