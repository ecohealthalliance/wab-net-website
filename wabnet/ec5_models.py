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
    x_25_Site_modification_x = models.TextField(verbose_name='Site modifications to accomodate tourists')
    x_26_Frequency_of_huma_x = models.TextField(verbose_name='Frequency of human visitation to the site')
    x_27_Specify_other_fre_x = models.TextField(verbose_name='Specify other frequency of human visitation')
    x_28_Evidence_of_human_x = models.TextField(verbose_name='Evidence of human disturbance at site (select all that apply)')
    x_29_Specify_Other_evi_x = models.TextField(verbose_name='Specify "Other" evidence of human disturbance at site')


class x_30_Site_photographs_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site photographs'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5b4ce68152e52'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_31_Site_photograph_1_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 1')
    x_32_Site_photograph_2_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 2')
    x_33_Site_photograph_3_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 3')
    x_34_Site_photograph_4_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph 4')
    x_35_Description_of_si_x = models.TextField(verbose_name='Description of site photograph')


class x_36_Site_video_option_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site video (optional)'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5bc0be2f6b832'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_37_Site_video_x = models.FileField(upload_to='ec5/', verbose_name='Site video')

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
    x_38_Date_of_trapping_x = models.TextField(verbose_name='Date of trapping event')
    x_40_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event began (nets opened)')
    x_41_Date_traps_closed_x = models.TextField(verbose_name='Date traps closed (may extend a day)')
    x_42_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event ended (nets closed)')
    x_43_Weather_condition_x = models.TextField(verbose_name='Weather conditions during trapping event')
    x_45_Number_of_26_mete_x = models.IntegerField(verbose_name='Number of 2.6 meter nets', blank=True, null=True)
    x_46_Number_of_4_meter_x = models.IntegerField(verbose_name='Number of 4 meter nets', blank=True, null=True)
    x_47_Number_of_6_meter_x = models.IntegerField(verbose_name='Number of 6 meter nets', blank=True, null=True)
    x_48_Number_of_9_meter_x = models.IntegerField(verbose_name='Number of 9 meter nets', blank=True, null=True)
    x_49_Number_of_harp_tr_x = models.IntegerField(verbose_name='Number of harp traps', blank=True, null=True)
    x_51_Page_1_x = models.FileField(upload_to='ec5/', verbose_name='Page 1')
    x_52_Page_2_x = models.FileField(upload_to='ec5/', verbose_name='Page 2')
    x_53_Page_3_x = models.FileField(upload_to='ec5/', verbose_name='Page 3')
    x_54_Page_4_x = models.FileField(upload_to='ec5/', verbose_name='Page 4')
    x_55_Page_5_x = models.FileField(upload_to='ec5/', verbose_name='Page 5')
    x_56_Page_6_x = models.FileField(upload_to='ec5/', verbose_name='Page 6')
    x_57_Page_7_x = models.FileField(upload_to='ec5/', verbose_name='Page 7')
    x_58_Page_8_x = models.FileField(upload_to='ec5/', verbose_name='Page 8')
    x_59_Field_notes_x = models.TextField(verbose_name='Field notes')

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
    x_61_ANIMAL_ID_eg_PK00_x = models.TextField(verbose_name='ANIMAL ID        [eg. PK0001] ')
    x_62_Bat_family_x = models.TextField(verbose_name='Bat family')
    x_63_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat family')
    x_64_Family_Emballonur_x = models.TextField(verbose_name='Family: Emballonuridae')
    x_65_Family_Hipposider_x = models.TextField(verbose_name='Family: Hipposideridae')
    x_66_Family_Megadermat_x = models.TextField(verbose_name='Family: Megadermatidae')
    x_67_Family_Miniopteri_x = models.TextField(verbose_name='Family: Miniopteridae')
    x_68_Family_Molossidae_x = models.TextField(verbose_name='Family: Molossidae')
    x_69_Family_Nycteridae_x = models.TextField(verbose_name='Family: Nycteridae')
    x_70_Family_Pteropodid_x = models.TextField(verbose_name='Family: Pteropodidae')
    x_71_Family_Rhinolophi_x = models.TextField(verbose_name='Family: Rhinolophidae')
    x_72_Family_Rhinopomat_x = models.TextField(verbose_name='Family: Rhinopomatidae')
    x_73_Family_Vespertili_x = models.TextField(verbose_name='Family: Vespertilionidae')
    x_74_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat species')
    x_75_Age_x = models.TextField(verbose_name='Age')
    x_76_Sex_x = models.TextField(verbose_name='Sex')
    x_77_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Male')
    x_78_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Female')
    x_80_Forearm_length_mm_x = models.TextField(verbose_name='Forearm length (mm)')
    x_81_Body_mass_g_x = models.TextField(verbose_name='Body mass (g)')
    x_82_Attached_pup_x = models.TextField(verbose_name='Attached pup?')
    x_83_Ear_length_mm_x = models.TextField(verbose_name='Ear length (mm)')
    x_84_Tail_length_mm_x = models.TextField(verbose_name='Tail length (mm)')
    x_85_Foot_length_mm_x = models.TextField(verbose_name='Foot length (mm)')
    x_86_Head_body_length_x = models.TextField(verbose_name='Head & body length (mm)')
    x_87_Other_morphologic_x = models.TextField(verbose_name='Other morphological measurements, be specific')
    x_89_Picture_1_x = models.FileField(upload_to='ec5/', verbose_name='Picture 1')
    x_90_Picture_2_x = models.FileField(upload_to='ec5/', verbose_name='Picture 2')
    x_91_Picture_3_x = models.FileField(upload_to='ec5/', verbose_name='Picture 3')
    x_92_Picture_4_x = models.FileField(upload_to='ec5/', verbose_name='Picture 4')
    x_93_Video_1_x = models.FileField(upload_to='ec5/', verbose_name='Video 1')
    x_94_Video_2_x = models.FileField(upload_to='ec5/', verbose_name='Video 2')
    x_95_Collect_diagnosti_x = models.TextField(verbose_name='Collect diagnostic samples - swabs, urine, feces, blood?')
    x_96_Collect_ORAL_swab_x = models.TextField(verbose_name='Collect ORAL swabs?')
    x_98_SAMPLE_1_Oral_swa_x = models.TextField(verbose_name='SAMPLE 1: Oral swab [AnimalID.OS1]')
    x_99_SAMPLE_2_Oral_swa_x = models.TextField(verbose_name='SAMPLE 2: Oral swab [AnimalID.OS2)')
    x_100_Collect_FECES_fr_x = models.TextField(verbose_name='Collect FECES (fresh) or RECTAL swabs?')
    x_102_Sample_1_SAMPLE_x = models.TextField(verbose_name='Sample 1: SAMPLE TYPE')
    x_103_Sample_2_SAMPLE_x = models.TextField(verbose_name='Sample 2: SAMPLE TYPE')
    x_104_Sample_1_STORAGE_x = models.TextField(verbose_name='Sample 1: STORAGE MEDIA')
    x_105_Sample_2_STORAGE_x = models.TextField(verbose_name='Sample 2: STORAGE MEDIA')
    x_106_Collect_URINE_UR_x = models.TextField(verbose_name='Collect URINE (UR) in RNALater?')
    x_107_Collect_BLOOD_x = models.TextField(verbose_name='Collect BLOOD?')
    x_109_Whole_blood_WB_s_x = models.TextField(verbose_name='Whole blood (WB) stored in RNAlater (R)')
    x_110_Whole_blood_WB_s_x = models.TextField(verbose_name='Whole blood (WB) stored in TRIZOL (T)')
    x_111_Estimate_microli_x = models.TextField(verbose_name='Estimate microliters of blood drawn')
    x_112_Blood_plasma_BP_x = models.TextField(verbose_name='Blood plasma (BP) stored in RNAlater (R)')
    x_113_Prepare_BLOOD_S_x = models.TextField(verbose_name='Prepare BLOOD - SMEAR?')
    x_114_Collect_WING_BIO_x = models.TextField(verbose_name='Collect WING BIOPSY PUNCH?')
    x_115_Collect_OTHER_sa_x = models.TextField(verbose_name='Collect OTHER samples (eg. ectoparasites)')
    x_116_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected')
    x_117_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected not included on the list')
    x_118_Acoustic_recordi_x = models.TextField(verbose_name='Acoustic recordings taken?')
    x_128_Necropsy_or_spec_x = models.TextField(verbose_name='Necropsy or specimen voucher performed?')
    x_130_Date_necropsy_pe_x = models.TextField(verbose_name='Date necropsy performed')
    x_131_Person_performin_x = models.TextField(verbose_name='Person performing the necropsy')
    x_132_Samples_collecte_x = models.TextField(verbose_name='Samples collected during necropsy (store in RNAlater)')
    x_133_Bat_prepared_as_x = models.TextField(verbose_name='Bat prepared as museum specimen?')
    x_134_If_yes_deposited_x = models.TextField(verbose_name='If yes, deposited at what facility?')
    x_135_Additional_infor_x = models.TextField(verbose_name='Additional information noted')


class x_119_Acoustic_recordi_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Acoustic recording information'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456e7bf94bc_5b4ce74352e58'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(BatData, on_delete=models.CASCADE)
    x_120_Recording_equipm_x = models.TextField(verbose_name='Recording equipment used')
    x_121_Site_conditions_x = models.TextField(verbose_name='Site conditions where recording was taken')
    x_122_Specify_other_si_x = models.TextField(verbose_name='Specify other site conditions')
    x_123_Recording_method_x = models.TextField(verbose_name='Recording method')
    x_124_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 1')
    x_125_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 2')
    x_126_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 3')
    x_127_File_numbers_typ_x = models.TextField(verbose_name='File number(s), typically xxxx.wav')

