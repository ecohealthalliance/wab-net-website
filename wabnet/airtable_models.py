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
    animal_id = models.TextField(verbose_name='Unique ANIMAL ID', null=False)
    date_rtpcr = models.DateTimeField(verbose_name='Date of RT-PCR', null=True)
    date_gel_electrophoresis = models.DateTimeField(verbose_name='Date of gel electrophoresis', null=True)
    gel_electrophoresis_results = models.TextField(verbose_name='Gel electrophoresis results')
    gel_electrophoresis_notes = models.TextField(verbose_name='Gel electrophoresis notes')
    gel_photo_labeled = models.TextField(verbose_name='Gel photo - labeled')
    date_sequenced = models.DateTimeField(verbose_name='Date of sequencing', null=True)
    sequencing_results = models.TextField(verbose_name='Sequencing results')
    sequencing_results_other = models.TextField(verbose_name='Sequencing results - if "Other"')
    sequencing_notes = models.TextField(verbose_name='Sequencing notes')
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


class Screening(models.Model):
    animal_id = models.TextField(verbose_name='Unique ANIMAL ID')
    animal_id_reentry = models.TextField(verbose_name='Unique ANIMAL ID (re-entry)')
    sample_id = models.TextField(verbose_name='Unique SAMPLE ID')
    sample_type = models.TextField(verbose_name='Sample type')
    sample_storage_media = models.TextField(verbose_name='Sample storage media')
    storage_facility = models.TextField(verbose_name='Storage facility')
    sample_condition = models.TextField(verbose_name='General notes on sample condition')
    lab_performing_testing = models.TextField(verbose_name='Laboratory performing testing')
    date_RNA_extraction = models.DateTimeField(verbose_name='Date of RNA extraction', null=True)
    RNA_extraction_method = models.TextField(verbose_name='RNA extraction method')
    performed_rtpcr_1 = models.TextField(verbose_name='Performed RT-PCR Method 1 [One-step RT-PCR + PCR]')
    date_rtpcr_1 = models.DateTimeField(verbose_name='Date RT-PCR Method 1 performed', null=True)
    performed_rtpcr_2 = models.TextField(verbose_name='Performed RT-PCR Method 2 [RT (cDNA) + PCR]? (RSS only)')
    date_rtpcr_2 = models.DateTimeField(verbose_name='Date RT-PCR Method 2 performed (RSS only)', null=True)
    date_gel_electrophoresis = models.DateTimeField(verbose_name='Date of gel electrophoresis', null=True)
    positive_control_1 = models.TextField(verbose_name='Positive control 1')
    positive_control_1_visible = models.TextField(verbose_name='Positive control 1 visible')
    positive_control_2 = models.TextField(verbose_name='Positive control 2')
    positive_control_2_visible = models.TextField(verbose_name='Positive control 2 visible')
    negative_control = models.TextField(verbose_name='Negative control')
    gel_electrophoresis_results = models.TextField(verbose_name='Gel electrophoresis results')
    gel_electrophoresis_notes_comments = models.TextField(verbose_name='Gel electrophoresis notes/comments')
    gel_photo_labeled = models.TextField(verbose_name='Gel photo - labeled')
    confirmation_test_type = models.TextField(verbose_name='Confirmation test type')
    date_confirmation_test = models.DateTimeField(verbose_name='Date of confirmation test', null=True)
    lab_performing_sequencing = models.TextField(verbose_name='Laboratory performing sequencing')
    sequencer_model = models.TextField(verbose_name='Sequencer model')
    confirmation_test_results = models.TextField(verbose_name='Confirmation test result')
    confirmation_test_results_other = models.TextField(verbose_name='Confirmation test result - if "Other"')
    confirmation_test_notes = models.TextField(verbose_name='Notes on confirmation tests')
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

class RawCovSequenceAb1(models.Model):
    airtable_id = models.TextField()
    url = models.TextField()
    filename = models.TextField()
    size = models.PositiveIntegerField()
    type = models.TextField()
    screening_parent = models.ForeignKey(Screening, on_delete=models.CASCADE)
