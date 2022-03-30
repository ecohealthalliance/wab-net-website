# These models were generated from an Epicollect 5 project via generate_models.py
from django.db import models
from ec5_tools import entity_keywords_model
from django.contrib.contenttypes.fields import GenericRelation

project_name = 'western-asia-bat-research'

class SiteData(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Field data forms'
    ec5_is_branch = False
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a'
    uuid = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    country = models.TextField(verbose_name='Country')
    x_3_Site_name_x = models.TextField(verbose_name='Site name')
    x_4_Site_location_GPS_x = models.TextField(verbose_name='Site location (GPS coords.)')
    x_5_Date_of_site_chara_x = models.TextField(verbose_name='Date of site characterization')
    x_6_Site_type_x = models.TextField(verbose_name='Site type')
    x_7_Specify_other_site_x = models.TextField(verbose_name='Specify other site type')
    x_8_Guano_present_at_s_x = models.TextField(verbose_name='Guano present at site?')
    x_9_Human_population_s_x = models.TextField(verbose_name='Human population size in 1-km radius of site:')
    x_10_Bathuman_interfac_x = models.TextField(verbose_name='Bat-human interface (check all that apply)')
    x_11_If_natural_area_w_x = models.TextField(verbose_name='If natural area, what is the setting?')
    x_12_If_forest_what_is_x = models.TextField(verbose_name='If forest, what is the estimated forest area?')
    x_13_If_forest_what_is_x = models.TextField(verbose_name='If forest, what is the condition of the forest?')
    x_14_Specify_Other_for_x = models.TextField(verbose_name='Specify "Other" forest condition')
    x_15_Trapping_at_a_cav_x = models.TextField(verbose_name='Trapping at a cave or mine?')
    x_16_If_cave_what_is_t_x = models.TextField(verbose_name='If cave, what is the estimated length of the cave?')
    x_17_If_cave_how_compl_x = models.TextField(verbose_name='If cave, how complex (spatially variable) is the cave?')
    x_18_Other_wildlife_ob_x = models.TextField(verbose_name='Other wildlife observed at the site?')
    x_19_List_other_wildli_x = models.TextField(verbose_name='List other wildlife observed, be specific')
    x_20_Domestic_animals_x = models.TextField(verbose_name='Domestic animals observed at the site?')
    x_21_List_domestic_ani_x = models.TextField(verbose_name='List domestic animals observed, be specific')
    x_22_Water_present_at_x = models.TextField(verbose_name='Water present at the site?')
    x_23_Is_water_shared_b_x = models.TextField(verbose_name='Is water shared between animals/wildlife and humans?')
    x_24_Site_accessibilit_x = models.TextField(verbose_name='Site accessibility')
    x_25_Site_modification_x = models.TextField(verbose_name='Site modifications to accommodate tourists')
    x_26_Other_site_modifi_x = models.TextField(verbose_name='Other site modifications to accommodate tourists, be specific')
    x_27_Frequency_of_huma_x = models.TextField(verbose_name='Frequency of human visitation to the site')
    x_28_Specify_other_fre_x = models.TextField(verbose_name='Specify other frequency of human visitation')
    x_29_Evidence_of_human_x = models.TextField(verbose_name='Evidence of human disturbance at site (select all that apply)')
    x_30_Specify_x = models.TextField(verbose_name='Specify ')

    def get_country(self):
        return self.country

class x_31_Site_photographs_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site photographs'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5b4ce68152e52'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_32_Site_photograph_1_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 1')
    x_33_Site_photograph_2_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 2')
    x_34_Site_photograph_3_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 3')
    x_35_Site_photograph_4_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 4')
    x_36_Description_of_si_x = models.TextField(verbose_name='Description of site photograph')

    def get_country(self):
        return self.parent.country

class x_37_Site_video_option_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site video (optional)'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5bc0be2f6b832'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_38_Site_video_x = models.FileField(upload_to='ec5/', verbose_name='Site video')

    def get_country(self):
        return self.parent.country

class TrappingEvent(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Trapping event information'
    ec5_is_branch = False
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456ba1f94aa'
    uuid = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_39_Date_of_trapping_x = models.TextField(verbose_name='Date of trapping event')
    x_41_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event began (nets opened)')
    x_42_Date_traps_closed_x = models.TextField(verbose_name='Date traps closed (may extend a day)')
    x_43_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event ended (nets closed)')
    x_44_Weather_condition_x = models.TextField(verbose_name='Weather conditions during trapping event')
    x_46_Number_of_26_mete_x = models.TextField(verbose_name='Number of 2.6 meter nets', null=True)
    x_47_Number_of_4_meter_x = models.TextField(verbose_name='Number of 4 meter nets', null=True)
    x_48_Number_of_6_meter_x = models.TextField(verbose_name='Number of 6 meter nets', null=True)
    x_49_Number_of_9_meter_x = models.TextField(verbose_name='Number of 9 meter nets', null=True)
    x_50_Number_of_12_mete_x = models.TextField(verbose_name='Number of 12 meter nets', null=True)
    x_51_Number_of_18_mete_x = models.TextField(verbose_name='Number of 18 meter nets', null=True)
    x_52_Number_of_harp_tr_x = models.TextField(verbose_name='Number of harp traps', null=True)
    x_54_Page_1_x = models.FileField(upload_to='ec5/', verbose_name='Page 1')
    x_55_Page_2_x = models.FileField(upload_to='ec5/', verbose_name='Page 2')
    x_56_Page_3_x = models.FileField(upload_to='ec5/', verbose_name='Page 3')
    x_57_Page_4_x = models.FileField(upload_to='ec5/', verbose_name='Page 4')
    x_58_Page_5_x = models.FileField(upload_to='ec5/', verbose_name='Page 5')
    x_59_Page_6_x = models.FileField(upload_to='ec5/', verbose_name='Page 6')
    x_60_Page_7_x = models.FileField(upload_to='ec5/', verbose_name='Page 7')
    x_61_Page_8_x = models.FileField(upload_to='ec5/', verbose_name='Page 8')
    x_62_Field_notes_x = models.TextField(verbose_name='Field notes')

    def get_country(self):
        return self.parent.country

class BatData(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Bat information'
    ec5_is_branch = False
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456e7bf94bc'
    uuid = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(TrappingEvent, on_delete=models.CASCADE)
    x_64_ANIMAL_ID_x = models.TextField(verbose_name='ANIMAL ID')
    x_65_Bat_family_x = models.TextField(verbose_name='Bat family')
    x_66_Specify_x = models.TextField(verbose_name='Specify ')
    x_67_Family_Emballonur_x = models.TextField(verbose_name='Family: Emballonuridae')
    x_68_Family_Hipposider_x = models.TextField(verbose_name='Family: Hipposideridae')
    x_69_Family_Megadermat_x = models.TextField(verbose_name='Family: Megadermatidae')
    x_70_Family_Miniopteri_x = models.TextField(verbose_name='Family: Miniopteridae')
    x_71_Family_Molossidae_x = models.TextField(verbose_name='Family: Molossidae')
    x_72_Family_Nycteridae_x = models.TextField(verbose_name='Family: Nycteridae')
    x_73_Family_Pteropodid_x = models.TextField(verbose_name='Family: Pteropodidae')
    x_74_Family_Rhinolophi_x = models.TextField(verbose_name='Family: Rhinolophidae')
    x_75_Family_Rhinonycte_x = models.TextField(verbose_name='Family: Rhinonycteridae')
    x_76_Family_Rhinopomat_x = models.TextField(verbose_name='Family: Rhinopomatidae')
    x_77_Family_Vespertili_x = models.TextField(verbose_name='Family: Vespertilionidae')
    x_78_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat species')
    x_79_Age_x = models.TextField(verbose_name='Age')
    x_80_Sex_x = models.TextField(verbose_name='Sex')
    x_81_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Male')
    x_82_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Female')
    x_84_Forearm_length_mm_x = models.TextField(verbose_name='Forearm length (mm)')
    x_85_Body_mass_g_x = models.TextField(verbose_name='Body mass (g)')
    x_86_Attached_pup_x = models.TextField(verbose_name='Attached pup?')
    x_87_Ear_length_mm_x = models.TextField(verbose_name='Ear length (mm)')
    x_88_Tail_length_mm_x = models.TextField(verbose_name='Tail length (mm)')
    x_89_Foot_length_mm_x = models.TextField(verbose_name='Foot length (mm)')
    x_90_Head_body_length_x = models.TextField(verbose_name='Head & body length (mm)')
    x_91_Other_morphologic_x = models.TextField(verbose_name='Other morphological measurements, be specific')
    x_93_Picture_1_x = models.FileField(upload_to='ec5/', verbose_name='Picture 1')
    x_94_Picture_2_x = models.FileField(upload_to='ec5/', verbose_name='Picture 2')
    x_95_Picture_3_x = models.FileField(upload_to='ec5/', verbose_name='Picture 3')
    x_96_Picture_4_x = models.FileField(upload_to='ec5/', verbose_name='Picture 4')
    x_97_Video_1_x = models.FileField(upload_to='ec5/', verbose_name='Video 1')
    x_98_Video_2_x = models.FileField(upload_to='ec5/', verbose_name='Video 2')
    x_99_Collect_diagnosti_x = models.TextField(verbose_name='Collect diagnostic samples - swabs, urine, feces, blood?')
    x_100_Collect_ORAL_swa_x = models.TextField(verbose_name='Collect ORAL swabs?')
    x_102_SAMPLE_1_Oral_sw_x = models.TextField(verbose_name='SAMPLE 1: Oral swab [AnimalID.OS1]')
    x_103_SAMPLE_2_Oral_sw_x = models.TextField(verbose_name='SAMPLE 2: Oral swab [AnimalID.OS2)')
    x_104_Collect_FECES_fr_x = models.TextField(verbose_name='Collect FECES (fresh) or RECTAL swabs?')
    x_106_Sample_1_SAMPLE_x = models.TextField(verbose_name='Sample 1: SAMPLE TYPE')
    x_107_Sample_2_SAMPLE_x = models.TextField(verbose_name='Sample 2: SAMPLE TYPE')
    x_108_Sample_1_STORAGE_x = models.TextField(verbose_name='Sample 1: STORAGE MEDIA')
    x_109_Sample_2_STORAGE_x = models.TextField(verbose_name='Sample 2: STORAGE MEDIA')
    x_110_Collect_URINE_UR_x = models.TextField(verbose_name='Collect URINE (UR) in RNALater?')
    x_111_Collect_BLOOD_x = models.TextField(verbose_name='Collect BLOOD?')
    x_113_Estimate_microli_x = models.IntegerField(verbose_name='Estimate microliters of blood drawn', blank=True, null=True)
    x_114_Whole_blood_WB_s_x = models.TextField(verbose_name='Whole blood (WB) stored in RNAlater')
    x_115_Whole_blood_WB_s_x = models.TextField(verbose_name='Whole blood (WB) stored in TRIzol ')
    x_116_Blood_serum_SER_x = models.TextField(verbose_name='Blood serum (SER) stored in PBS')
    x_117_Blood_clot_RBC_s_x = models.TextField(verbose_name='Blood clot (RBC) stored in RNAlater')
    x_118_Prepare_BLOOD_S_x = models.TextField(verbose_name='Prepare BLOOD - SMEAR?')
    x_119_Collect_WING_BIO_x = models.TextField(verbose_name='Collect WING BIOPSY PUNCH?')
    x_120_Collect_OTHER_sa_x = models.TextField(verbose_name='Collect OTHER samples (eg. ectoparasites)')
    x_121_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected')
    x_122_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected not included on the list')
    x_123_Acoustic_recordi_x = models.TextField(verbose_name='Acoustic recordings taken?')
    x_133_Necropsy_or_spec_x = models.TextField(verbose_name='Necropsy or specimen voucher performed?')
    x_135_Date_necropsy_pe_x = models.TextField(verbose_name='Date necropsy performed')
    x_136_Person_performin_x = models.TextField(verbose_name='Person performing the necropsy')
    x_137_Samples_collecte_x = models.TextField(verbose_name='Samples collected during necropsy (store in RNAlater)')
    x_138_Bat_prepared_as_x = models.TextField(verbose_name='Bat prepared as museum specimen?')
    x_139_If_yes_deposited_x = models.TextField(verbose_name='If yes, deposited at what facility?')
    x_140_Additional_infor_x = models.TextField(verbose_name='Additional information noted')

    def get_country(self):
        return self.parent.parent.country

    def get_long_name(self, short_name):
        if short_name == 'ANIMAL_ID':
            targ = '_ANIMAL_ID_x'
        else:
            raise ValueError('ec5_models.py:BatData():get_long_name: short name __{}__ not supported'.format(short_name))

        for f in BatData._meta.get_fields():
            if targ in getattr(f, 'name'):
                return getattr(f, 'name')


class x_124_Acoustic_recordi_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Acoustic recording information'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456e7bf94bc_5b4ce74352e58'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(BatData, on_delete=models.CASCADE)
    x_125_Recording_equipm_x = models.TextField(verbose_name='Recording equipment used')
    x_126_Site_conditions_x = models.TextField(verbose_name='Site conditions where recording was taken')
    x_127_Specify_other_si_x = models.TextField(verbose_name='Specify other site conditions')
    x_128_Recording_method_x = models.TextField(verbose_name='Recording method')
    x_129_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 1')
    x_130_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 2')
    x_131_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 3')
    x_132_File_numbers_typ_x = models.TextField(verbose_name='File number(s), typically xxxx.wav')

    def get_country(self):
        return self.parent.parent.parent.country
