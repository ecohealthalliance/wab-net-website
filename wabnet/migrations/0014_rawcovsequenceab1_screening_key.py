# Generated by Django 3.0.7 on 2020-09-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0013_auto_20200910_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawcovsequenceab1',
            name='screening_key',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
