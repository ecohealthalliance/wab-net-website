# Generated by Django 3.1.7 on 2021-10-22 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0029_auto_20211022_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screening',
            name='rerun2_date_rtpcr_1',
            field=models.DateTimeField(null=True, verbose_name='RE-RUN 2  Date of RT-PCR'),
        ),
    ]
