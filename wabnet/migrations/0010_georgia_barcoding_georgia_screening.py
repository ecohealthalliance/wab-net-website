# Generated by Django 3.0.7 on 2020-08-13 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wabnet', '0009_auto_20200713_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Georgia_barcoding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_id', models.TextField(verbose_name='Unique ANIMAL ID')),
                ('date_rtpcr', models.DateTimeField(null=True, verbose_name='Date of RT-PCR')),
                ('date_gel_electrophoresis', models.DateTimeField(null=True, verbose_name='Date of gel electrophoresis')),
                ('gel_electrophoresis_results', models.TextField(verbose_name='Gel electrophoresis results')),
                ('gel_electrophoresis_notes', models.TextField(verbose_name='Gel electrophoresis notes')),
                ('gel_photo_labeled', models.TextField(verbose_name='Gel photo - labeled')),
                ('date_sequenced', models.DateTimeField(null=True, verbose_name='Date of sequencing')),
                ('sequencing_results', models.TextField(verbose_name='Sequencing results')),
                ('sequencing_results_other', models.TextField(verbose_name='Sequencing results - if "Other"')),
                ('sequencing_notes', models.TextField(verbose_name='Sequencing notes')),
                ('raw_host_sequence_txt', models.TextField(verbose_name='Raw host sequence - .txt files')),
                ('raw_host_sequence_ab1', models.TextField(verbose_name='Raw host sequence - .ab1 files')),
                ('raw_host_sequence_pdf', models.TextField(verbose_name='Raw host sequence - .pdf files')),
                ('aligned_host_seuqence_submitted_to_blast', models.TextField(verbose_name='Aligned host sequence (.fasta file) submitted to BLAST')),
                ('host_identified_blast', models.TextField(verbose_name='Host species identified using BLAST')),
                ('host_identified_blast_other', models.TextField(verbose_name='Host species identified using BLAST - if Other')),
                ('query_cover_top_BLAST_match', models.FloatField(null=True, verbose_name='Query cover (%) for top BLAST match')),
                ('percent_identity_top_BLAST_match', models.FloatField(null=True, verbose_name='Percent identity (%) for top BLAST match')),
                ('screenshot_top_5_BLAST_matches', models.TextField(verbose_name='Screenshot photo of top 5 BLAST matches')),
                ('cov_screening_data', models.TextField(verbose_name='CoV Screening Data')),
            ],
        ),
        migrations.CreateModel(
            name='Georgia_screening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_id', models.TextField(verbose_name='Unique ANIMAL ID')),
                ('animal_id_reentry', models.TextField(verbose_name='Unique ANIMAL ID (re-entry)')),
                ('sample_id', models.TextField(verbose_name='Unique SAMPLE ID')),
                ('sample_type', models.TextField(verbose_name='Sample type')),
                ('sample_storage_media', models.TextField(verbose_name='Sample storage media')),
                ('storage_facility', models.TextField(verbose_name='Storage facility')),
                ('sample_condition', models.TextField(verbose_name='General notes on sample condition')),
                ('lab_performing_testing', models.TextField(verbose_name='Laboratory performing testing')),
                ('date_RNA_extraction', models.DateTimeField(null=True, verbose_name='Date of RNA extraction')),
                ('RNA_extraction_method', models.TextField(verbose_name='RNA extraction method')),
                ('performed_rtpcr_1', models.TextField(verbose_name='Performed RT-PCR Method 1 [One-step RT-PCR + PCR]')),
                ('date_rtpcr_1', models.DateTimeField(null=True, verbose_name='Date RT-PCR Method 1 performed')),
                ('performed_rtpcr_2', models.TextField(verbose_name='Performed RT-PCR Method 2 [RT (cDNA) + PCR]? (RSS only)')),
                ('date_rtpcr_2', models.DateTimeField(null=True, verbose_name='Date RT-PCR Method 2 performed (RSS only)')),
                ('date_gel_electrophoresis', models.DateTimeField(null=True, verbose_name='Date of gel electrophoresis')),
                ('positive_control_1', models.TextField(verbose_name='Positive control 1')),
                ('positive_control_1_visible', models.TextField(verbose_name='Positive control 1 visible')),
                ('positive_control_2', models.TextField(verbose_name='Positive control 2')),
                ('positive_control_2_visible', models.TextField(verbose_name='Positive control 2 visible')),
                ('negative_control', models.TextField(verbose_name='Negative control')),
                ('gel_electrophoresis_results', models.TextField(verbose_name='Gel electrophoresis results')),
                ('gel_electrophoresis_notes_comments', models.TextField(verbose_name='Gel electrophoresis notes/comments')),
                ('gel_photo_labeled', models.TextField(verbose_name='Gel photo - labeled')),
                ('confirmation_test_type', models.TextField(verbose_name='Confirmation test type')),
                ('date_confirmation_test', models.DateTimeField(null=True, verbose_name='Date of confirmation test')),
                ('lab_performing_sequencing', models.TextField(verbose_name='Laboratory performing sequencing')),
                ('sequencer_model', models.TextField(verbose_name='Sequencer model')),
                ('confirmation_test_results', models.TextField(verbose_name='Confirmation test result')),
                ('confirmation_test_results_other', models.TextField(verbose_name='Confirmation test result - if "Other"')),
                ('confirmation_test_notes', models.TextField(verbose_name='Notes on confirmation tests')),
                ('raw_cov_sequence_txt', models.TextField(verbose_name='Raw CoV sequence - .txt files')),
                ('raw_cov_sequence_ab1', models.TextField(verbose_name='Raw CoV sequence - .ab1 files')),
                ('raw_cov_sequence_pdf', models.TextField(verbose_name='Raw CoV sequence - .pdf files')),
                ('aligned_cov_seuqence_submitted_to_blast', models.TextField(null=True, verbose_name='Aligned CoV sequence (.fasta file) submitted to BLAST')),
                ('coronavirus_identified_blast', models.TextField(verbose_name='Coronavirus identified by BLAST')),
                ('query_cover_top_BLAST_match', models.FloatField(null=True, verbose_name='Query cover (%) for top BLAST match')),
                ('percent_identity_top_BLAST_match', models.FloatField(null=True, verbose_name='Percent identity (%) for top BLAST match')),
                ('screenshot_top_5_BLAST_matches', models.TextField(verbose_name='Screenshot photo of top 5 BLAST matches')),
                ('barcoding_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wabnet.Georgia_barcoding')),
            ],
        ),
    ]
