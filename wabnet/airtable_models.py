# These models were generated from an Epicollect 5 project via generate_models.py
from django.db import models
from ec5_tools import entity_keywords_model
from django.contrib.contenttypes.fields import GenericRelation

import logging

logger = logging.getLogger(__name__)
hdlr = logging.FileHandler('./log.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Notes:
# 1) animal_id has a duplicate field in the screening tables for verification
# 2) animal_id col in both tables but barcoding table also has CoV Screening
#    Data col that associates with parent table (foreign key)

class Barcoding(models.Model):
    animal_id = models.TextField(verbose_name='ANIMAL ID', null=False)
    sample_id = models.TextField(verbose_name='SAMPLE ID', null=True)
    sample_type = models.TextField(verbose_name='Sample type', null=True)
    date_RNA_extraction = models.DateTimeField(verbose_name='Date of RNA extraction', null=True)
    rerun_sample_id = models.TextField(verbose_name='RE-RUN SAMPLE ID', null=True)
    rerun_sample_type = models.TextField(verbose_name='RE-RUN Sample type', null=True)
    country = models.TextField(verbose_name='Country', null=False, default='not set')
    date_rtpcr = models.DateTimeField(verbose_name='Date of RT-PCR', null=True)
    date_gel_electrophoresis = models.DateTimeField(verbose_name='Date of gel electrophoresis', null=True)
    gel_electrophoresis_results = models.TextField(verbose_name='Gel electrophoresis result')
    gel_electrophoresis_notes = models.TextField(verbose_name='Gel electrophoresis notes')
    gel_photo_labeled = models.TextField(verbose_name='Gel photo - labeled')
    date_sequenced = models.DateTimeField(verbose_name='Date of sequencing', null=True)
    sequencing_results = models.TextField(verbose_name='Sequencing result')
    sequencing_results_other = models.TextField(verbose_name='Sequencing result - if "Other"')
    raw_host_sequence_txt = models.TextField(verbose_name='Raw host sequence - .txt files')
    raw_host_sequence_ab1 = models.TextField(verbose_name='Raw host sequence - .ab1 files')
    raw_host_sequence_pdf = models.TextField(verbose_name='Raw host sequence - .pdf files')
    aligned_host_seuqence_submitted_to_blast = models.TextField(verbose_name='Aligned host sequence (.fasta file) submitted to BLAST')
    host_identified_blast = models.TextField(verbose_name='Host species identified using BLAST')
    host_identified_blast_other = models.TextField(verbose_name='Host species identified using BLAST - if Other')
    query_cover_top_BLAST_match = models.FloatField(verbose_name='Query cover (%) for top BLAST match', null=True)
    percent_identity_top_BLAST_match = models.FloatField(verbose_name='Percent identity (%) for top BLAST match', null=True)
    screenshot_top_5_BLAST_matches = models.TextField(verbose_name='Screenshot photo of top 5 BLAST matches')
    #cov_screening_data = models.ForeignKey(Georgia_screening, on_delete=models.CASCADE, verbose_name='CoV Screening Data')
    rerun_sample = models.TextField(verbose_name='Was sample RE-RUN?', null=True)
    rerun_sample_id = models.TextField(verbose_name='RE-RUN SAMPLE ID', null=True)
    rerun_sample_type = models.TextField(verbose_name='RE-RUN Sample type', null=True)
    rerun_date_RNA_extraction = models.DateTimeField(verbose_name='RE-RUN Date of RNA extraction', null=True)
    rerun_date_rtpcr = models.DateTimeField(verbose_name='RE-RUN Date of RT-PCR', null=True)
    rerun_date_gel_electrophoresis = models.DateTimeField(verbose_name='RE-RUN Date of gel electrophoresis', null=True)
    rerun_gel_electrophoresis_results = models.TextField(verbose_name='RE-RUN Gel electrophoresis result', null=True)
    rerun_gel_photo_labeled = models.TextField(verbose_name='RE-RUN Gel photo - labeled', null=True)
    rerun_date_sequenced = models.DateTimeField(verbose_name='RE-RUN Date of sequencing', null=True)
    rerun_sequencing_results = models.TextField(verbose_name='RE-RUN Sequencing result', null=True)
    rerun_sequencing_results_other = models.TextField(verbose_name='RE-RUN Sequencing result - if "Other"', null=True)
    rerun_raw_host_sequence_txt = models.TextField(verbose_name='RE-RUN Raw host sequence - .txt files', null=True)
    rerun_raw_host_sequence_ab1 = models.TextField(verbose_name='RE-RUN Raw host sequence - .ab1 files', null=True)
    rerun_raw_host_sequence_pdf = models.TextField(verbose_name='RE-RUN Raw host sequence - .pdf files', null=True)
    rerun_aligned_cov_seuqence_submitted_to_blast = models.TextField(verbose_name='RE-RUN Aligned host sequence (.fasta file) submitted to BLAST', null=True)
    rerun_host_identified_blast = models.TextField(verbose_name='RE-RUN Host species identified using BLAST', null=True)
    rerun_query_cover_top_BLAST_match = models.FloatField(verbose_name='RE-RUN Query cover (%) for top BLAST match', null=True)
    rerun_percent_identity_top_BLAST_match = models.FloatField(verbose_name='RE-RUN Percent identity (%) for top BLAST match', null=True)
    rerun_screenshot_top_5_BLAST_matches = models.TextField(verbose_name='RE-RUN Screenshot photo of top 5 BLAST matches', null=True)

    rerun2_sample = models.TextField(verbose_name='Was sample RE-RUN again?', null=True)
    rerun2_sample_id = models.TextField(verbose_name='RE-RUN 2 SAMPLE ID', null=True)
    rerun2_sample_type = models.TextField(verbose_name='RE-RUN 2 Sample type', null=True)
    rerun2_date_RNA_extraction = models.DateTimeField(verbose_name='RE-RUN 2 Date of RNA extraction', null=True)
    rerun2_date_rtpcr = models.DateTimeField(verbose_name='RE-RUN 2 Date of RT-PCR', null=True)
    rerun2_date_gel_electrophoresis = models.DateTimeField(verbose_name='RE-RUN 2 Date of gel electrophoresis', null=True)
    rerun2_gel_electrophoresis_results = models.TextField(verbose_name='RE-RUN 2 Gel electrophoresis result', null=True)
    rerun2_gel_photo_labeled = models.TextField(verbose_name='RE-RUN 2 Gel photo - labeled', null=True)
    rerun2_date_sequenced = models.DateTimeField(verbose_name='RE-RUN 2 Date of sequencing', null=True)
    rerun2_sequencing_results = models.TextField(verbose_name='RE-RUN 2 Sequencing result', null=True)
    rerun2_sequencing_results_other = models.TextField(verbose_name='RE-RUN 2 Sequencing result - if "Other"', null=True)
    rerun2_raw_host_sequence_txt = models.TextField(verbose_name='RE-RUN 2 Raw host sequence - .txt files', null=True)
    rerun2_raw_host_sequence_ab1 = models.TextField(verbose_name='RE-RUN 2 Raw host sequence - .ab1 files', null=True)
    rerun2_raw_host_sequence_pdf = models.TextField(verbose_name='RE-RUN 2 Raw host sequence - .pdf files', null=True)
    rerun2_aligned_cov_seuqence_submitted_to_blast = models.TextField(verbose_name='RE-RUN 2 Aligned host sequence (.fasta file) submitted to BLAST', null=True)
    rerun2_host_identified_blast = models.TextField(verbose_name='RE-RUN 2 Host species identified using BLAST', null=True)
    rerun2_query_cover_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 2 Query cover (%) for top BLAST match', null=True)
    rerun2_percent_identity_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 2 Percent identity (%) for top BLAST match', null=True)
    rerun2_screenshot_top_5_BLAST_matches = models.TextField(verbose_name='RE-RUN 2 Screenshot photo of top 5 BLAST matches', null=True)

    rerun3_sample = models.TextField(verbose_name='Was sample RE-RUN a 3rd time?', null=True)
    rerun3_sample_id = models.TextField(verbose_name='RE-RUN 3 SAMPLE ID', null=True)
    rerun3_sample_type = models.TextField(verbose_name='RE-RUN 3 Sample type', null=True)
    rerun3_date_RNA_extraction = models.DateTimeField(verbose_name='RE-RUN 3 Date of RNA extraction', null=True)
    rerun3_date_rtpcr = models.DateTimeField(verbose_name='RE-RUN 3 Date of RT-PCR', null=True)
    rerun3_date_gel_electrophoresis = models.DateTimeField(verbose_name='RE-RUN 3 Date of gel electrophoresis', null=True)
    rerun3_gel_electrophoresis_results = models.TextField(verbose_name='RE-RUN 3 Gel electrophoresis result', null=True)
    rerun3_gel_photo_labeled = models.TextField(verbose_name='RE-RUN 3 Gel photo - labeled', null=True)
    rerun3_date_sequenced = models.DateTimeField(verbose_name='RE-RUN 3 Date of sequencing', null=True)
    rerun3_sequencing_results = models.TextField(verbose_name='RE-RUN 3 Sequencing result', null=True)
    rerun3_sequencing_results_other = models.TextField(verbose_name='RE-RUN 3 Sequencing result - if "Other"', null=True)
    rerun3_raw_host_sequence_txt = models.TextField(verbose_name='RE-RUN 3 Raw host sequence - .txt files', null=True)
    rerun3_raw_host_sequence_ab1 = models.TextField(verbose_name='RE-RUN 3 Raw host sequence - .ab1 files', null=True)
    rerun3_raw_host_sequence_pdf = models.TextField(verbose_name='RE-RUN 3 Raw host sequence - .pdf files', null=True)
    rerun3_aligned_cov_seuqence_submitted_to_blast = models.TextField(verbose_name='RE-RUN 3 Aligned host sequence (.fasta file) submitted to BLAST', null=True)
    rerun3_host_identified_blast = models.TextField(verbose_name='RE-RUN 3 Host species identified using BLAST', null=True)
    rerun3_query_cover_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 3 Query cover (%) for top BLAST match', null=True)
    rerun3_percent_identity_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 3 Percent identity (%) for top BLAST match', null=True)
    rerun3_screenshot_top_5_BLAST_matches = models.TextField(verbose_name='RE-RUN 3 Screenshot photo of top 5 BLAST matches', null=True)

    primer_set = models.TextField(verbose_name='Primer set used', null=True)

    cov_screening_data = models.TextField(verbose_name='CoV Screening Data', null=False)

    def get_name_from_verbose(verbose_name):
        #return Georgia_barcoding._meta.get_field(animal_id).verbose_name.title()
        for f in Barcoding._meta.get_fields():
            if hasattr(f, 'verbose_name'):
                curr_verbose_name = getattr(f, 'verbose_name')
                if curr_verbose_name == verbose_name:
                    return getattr(f, 'name')
        logger.info('Error: airtable_modes.py: get_name_from_verbose():verbose_name __{}__ not found!!'.format(verbose_name))
        raise ValueError('airtable_models.py:Barcoding():verbose name __{}__ not found'.format(verbose_name))

    def get_verbose_from_name(var_name):
        verbose_name = ''
        for f in Barcoding._meta.get_fields():
            if f.name.split('.')[-1] == var_name:
                if hasattr(f, 'verbose_name'):
                    verbose_name = getattr(f, 'verbose_name')
        return verbose_name

    def get_country(self):
        return self.country

class Screening(models.Model):
    animal_id = models.TextField(verbose_name='ANIMAL ID')
    animal_id_reentry = models.TextField(verbose_name='ANIMAL ID (re-entry)')
    country = models.TextField(verbose_name='Country', null=False, default='not set')
    sample_id = models.TextField(verbose_name='SAMPLE ID')
    sample_type = models.TextField(verbose_name='Sample type')
    sample_storage_media = models.TextField(verbose_name='Sample storage media')
    lab_performing_testing = models.TextField(verbose_name='Laboratory performing testing')
    date_RNA_extraction = models.DateTimeField(verbose_name='Date of RNA extraction', null=True)
    RNA_extraction_method = models.TextField(verbose_name='RNA extraction method')
    date_rtpcr_1 = models.DateTimeField(verbose_name='Date of RT-PCR', null=True)
    date_gel_electrophoresis = models.DateTimeField(verbose_name='Date of gel electrophoresis', null=True)
    positive_control = models.TextField(verbose_name='Positive control', null=True)
    negative_control = models.TextField(verbose_name='Negative control')
    gel_electrophoresis_results = models.TextField(verbose_name='Gel electrophoresis result')
    gel_electrophoresis_notes_comments = models.TextField(verbose_name='Gel electrophoresis notes')
    gel_photo_labeled = models.TextField(verbose_name='Gel photo - labeled')
    confirmation_test_type = models.TextField(verbose_name='Confirmation test type')
    date_confirmation_test = models.DateTimeField(verbose_name='Date of sequencing', null=True)
    lab_performing_sequencing = models.TextField(verbose_name='Laboratory performing sequencing')
    sequencer_model = models.TextField(verbose_name='Sequencer model')
    confirmation_test_results = models.TextField(verbose_name='Sequencing result')
    confirmation_test_results_other = models.TextField(verbose_name='Sequencing result - if "Other"')
    raw_cov_sequence_txt = models.TextField(verbose_name='Raw CoV sequence - .txt files')
    raw_cov_sequence_ab1 = models.TextField(verbose_name='Raw CoV sequence - .ab1 files')
    raw_cov_sequence_pdf = models.TextField(verbose_name='Raw CoV sequence - .pdf files')
    #aligned_cov_sequence_submitted_to_blast = models.ForeignKey(Georgia_aligned_cov_seuqence_submitted_to_blast, on_delete=models.CASCADE, verbose_name='Aligned CoV sequence (.fasta file) submitted to BLAST', null=True)
    aligned_cov_sequence_submitted_to_blast = models.TextField(verbose_name='Aligned CoV sequence (.fasta file) submitted to BLAST', null=True)
    coronavirus_identified_blast = models.TextField(verbose_name='Coronavirus identified by BLAST')
    query_cover_top_BLAST_match = models.FloatField(verbose_name='Query cover (%) for top BLAST match', null=True)
    percent_identity_top_BLAST_match = models.FloatField(verbose_name='Percent identity (%) for top BLAST match', null=True)
    screenshot_top_5_BLAST_matches = models.TextField(verbose_name='Screenshot photo of top 5 BLAST matches')
    barcoding_record = models.ForeignKey(Barcoding, on_delete=models.CASCADE)
    rerun_sample = models.TextField(verbose_name='Was sample RE-RUN?', null=True)
    rerun_sample_id = models.TextField(verbose_name='RE-RUN SAMPLE ID', null=True)
    rerun_sample_type = models.TextField(verbose_name='RE-RUN Sample type', null=True)
    rerun_sample_storage_media = models.TextField(verbose_name='RE-RUN Sample storage media', null=True)
    rerun_date_RNA_extraction = models.DateTimeField(verbose_name='RE-RUN Date of RNA extraction', null=True)
    rerun_RNA_extraction_method = models.TextField(verbose_name='RE-RUN RNA extraction method', null=True)
    rerun_date_rtpcr_1 = models.DateTimeField(verbose_name='RE-RUN Date of RT-PCR', null=True)
    rerun_date_gel_electrophoresis = models.DateTimeField(verbose_name='RE-RUN Date of gel electrophoresis', null=True)
    rerun_positive_control = models.TextField(verbose_name='RE-RUN Positive control', null=True)
    rerun_negative_control = models.TextField(verbose_name='RE-RUN Negative control', null=True)
    rerun_gel_electrophoresis_results = models.TextField(verbose_name='RE-RUN Gel electrophoresis result', null=True)
    rerun_gel_photo_labeled = models.TextField(verbose_name='RE-RUN Gel photo - labeled', null=True)
    rerun_date_confirmation_test = models.DateTimeField(verbose_name='RE-RUN Date of sequencing', null=True)
    rerun_confirmation_test_results = models.TextField(verbose_name='RE-RUN Sequencing result', null=True)
    rerun_confirmation_test_results_other = models.TextField(verbose_name='RE-RUN Sequencing result - if "Other"', null=True)
    rerun_raw_cov_sequence_txt = models.TextField(verbose_name='RE-RUN Raw CoV sequence - .txt files', null=True)
    rerun_raw_cov_sequence_ab1 = models.TextField(verbose_name='RE-RUN Raw CoV sequence - .ab1 files', null=True)
    rerun_raw_cov_sequence_pdf = models.TextField(verbose_name='RE-RUN Raw CoV sequence - .pdf files', null=True)
    rerun_aligned_cov_sequence_submitted_to_blast = models.TextField(verbose_name='RE-RUN Aligned CoV sequence (.fasta file) submitted to BLAST', null=True)
    rerun_coronavirus_identified_blast = models.TextField(verbose_name='RE-RUN Coronavirus identified by BLAST', null=True)
    rerun_query_cover_top_BLAST_match = models.FloatField(verbose_name='RE-RUN Query cover (%) for top BLAST match', null=True)
    rerun_percent_identity_top_BLAST_match = models.FloatField(verbose_name='RE-RUN Percent identity (%) for top BLAST match', null=True)
    rerun_screenshot_top_5_BLAST_matches = models.TextField(verbose_name='RE-RUN Screenshot photo of top 5 BLAST matches', null=True)

    rerun2_sample = models.TextField(verbose_name='Was sample RE-RUN again?', null=True)
    rerun2_sample_id = models.TextField(verbose_name='RE-RUN 2 SAMPLE ID', null=True)
    rerun2_sample_type = models.TextField(verbose_name='RE-RUN 2 Sample type', null=True)
    rerun2_sample_storage_media = models.TextField(verbose_name='RE-RUN 2 Sample storage media', null=True)
    rerun2_date_RNA_extraction = models.DateTimeField(verbose_name='RE-RUN 2 Date of RNA extraction', null=True)
    rerun2_RNA_extraction_method = models.TextField(verbose_name='RE-RUN 2 RNA extraction method', null=True)
    rerun2_date_rtpcr_1 = models.DateTimeField(verbose_name='RE-RUN 2  Date of RT-PCR', null=True)
    rerun2_date_gel_electrophoresis = models.DateTimeField(verbose_name='RE-RUN 2 Date of gel electrophoresis', null=True)
    rerun2_positive_control = models.TextField(verbose_name='RE-RUN 2 Positive control', null=True)
    rerun2_negative_control = models.TextField(verbose_name='RE-RUN 2 Negative control', null=True)
    rerun2_gel_electrophoresis_results = models.TextField(verbose_name='RE-RUN 2 Gel electrophoresis result', null=True)
    rerun2_gel_photo_labeled = models.TextField(verbose_name='RE-RUN 2 Gel photo - labeled', null=True)
    rerun2_date_confirmation_test = models.DateTimeField(verbose_name='RE-RUN 2 Date of sequencing', null=True)
    rerun2_confirmation_test_results = models.TextField(verbose_name='RE-RUN 2 Sequencing result', null=True)
    rerun2_confirmation_test_results_other = models.TextField(verbose_name='RE-RUN 2 Sequencing result - if "Other"', null=True)
    rerun2_raw_cov_sequence_txt = models.TextField(verbose_name='RE-RUN 2 Raw CoV sequence - .txt files', null=True)
    rerun2_raw_cov_sequence_ab1 = models.TextField(verbose_name='RE-RUN 2 Raw CoV sequence - .ab1 files', null=True)
    rerun2_raw_cov_sequence_pdf = models.TextField(verbose_name='RE-RUN 2 Raw CoV sequence - .pdf files', null=True)
    rerun2_aligned_cov_sequence_submitted_to_blast = models.TextField(verbose_name='RE-RUN 2 Aligned CoV sequence (.fasta file) submitted to BLAST', null=True)
    rerun2_coronavirus_identified_blast = models.TextField(verbose_name='RE-RUN 2 Coronavirus identified by BLAST', null=True)
    rerun2_query_cover_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 2 Query cover (%) for top BLAST match', null=True)
    rerun2_percent_identity_top_BLAST_match = models.FloatField(verbose_name='RE-RUN 2 Percent identity (%) for top BLAST match', null=True)
    rerun2_screenshot_top_5_BLAST_matches = models.TextField(verbose_name='RE-RUN 2 Screenshot photo of top 5 BLAST matches', null=True)

    # FIX: don't duplicate this method for all classes!!
    #      https://stackoverflow.com/questions/45189066/define-methods-for-multiple-classes
    def get_name_from_verbose(verbose_name):
        for f in Screening._meta.get_fields():
            if hasattr(f, 'verbose_name'):
                curr_verbose_name = getattr(f, 'verbose_name')
                if curr_verbose_name == verbose_name:
                    return getattr(f, 'name')
        # return None if verbose_name not found
        logger.info('Error: airtable_modes.py: get_name_from_verbose(): verbose_name __{}__ not found!!'.format(verbose_name))
        raise ValueError('airtable_models.py:Screening():verbose name __{}__ not found'.format(verbose_name))

    def get_verbose_from_name(var_name):
        verbose_name = ''
        for f in Screening._meta.get_fields():
            if f.name.split('.')[-1] == var_name:
                if hasattr(f, 'verbose_name'):
                    verbose_name = getattr(f, 'verbose_name')
        return verbose_name

    def get_country(self):
        return self.country


class RawCovSequenceAb1(models.Model):
    airtable_id = models.TextField()
    url = models.TextField()
    filename = models.TextField()
    size = models.PositiveIntegerField()
    type = models.TextField()
    screening_parent = models.ForeignKey(Screening, on_delete=models.CASCADE)
    screening_key = models.TextField()
