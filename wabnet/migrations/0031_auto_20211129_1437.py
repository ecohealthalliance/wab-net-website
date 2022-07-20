# Generated by Django 3.1.7 on 2021-11-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0030_auto_20211022_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_aligned_cov_seuqence_submitted_to_blast',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Aligned host sequence (.fasta file) submitted to BLAST'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_date_gel_electrophoresis',
            field=models.DateTimeField(null=True, verbose_name='RE-RUN 2 Date of gel electrophoresis'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_date_rtpcr',
            field=models.DateTimeField(null=True, verbose_name='RE-RUN 2 Date of RT-PCR'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_date_sequenced',
            field=models.DateTimeField(null=True, verbose_name='RE-RUN 2 Date of sequencing'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_gel_electrophoresis_results',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Gel electrophoresis result'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_gel_photo_labeled',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Gel photo - labeled'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_host_identified_blast',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Host species identified using BLAST'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_percent_identity_top_BLAST_match',
            field=models.FloatField(null=True, verbose_name='RE-RUN 2 Percent identity (%) for top BLAST match'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_query_cover_top_BLAST_match',
            field=models.FloatField(null=True, verbose_name='RE-RUN 2 Query cover (%) for top BLAST match'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_raw_host_sequence_ab1',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Raw host sequence - .ab1 files'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_raw_host_sequence_pdf',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Raw host sequence - .pdf files'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_raw_host_sequence_txt',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Raw host sequence - .txt files'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_sample',
            field=models.TextField(null=True, verbose_name='Was sample RE-RUN 2 again ?'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_screenshot_top_5_BLAST_matches',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Screenshot photo of top 5 BLAST matches'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_sequencing_results',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Sequencing result'),
        ),
        migrations.AddField(
            model_name='barcoding',
            name='rerun2_sequencing_results_other',
            field=models.TextField(null=True, verbose_name='RE-RUN 2 Sequencing result - if "Other"'),
        ),
    ]
