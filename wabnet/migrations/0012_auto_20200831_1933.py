# Generated by Django 3.0.7 on 2020-08-31 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0011_rawcovsequenceab1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='georgia_screening',
            old_name='aligned_cov_seuqence_submitted_to_blast',
            new_name='aligned_cov_sequence_submitted_to_blast',
        ),
    ]
