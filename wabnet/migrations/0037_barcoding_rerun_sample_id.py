# Generated by Django 3.1.7 on 2022-03-21 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0036_barcoding_date_rna_extraction'),
    ]

    operations = [
        migrations.AddField(
            model_name='barcoding',
            name='rerun_sample_id',
            field=models.TextField(null=True, verbose_name='RE-RUN SAMPLE ID'),
        ),
    ]
