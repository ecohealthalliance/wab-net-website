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
    x_27_Evidence_of_human_x = models.TextField(verbose_name='Evidence of human disturbance at site (select all that apply)')
    x_28_Specify_Other_evi_x = models.TextField(verbose_name='Specify "Other" evidence of human disturbance at site')


class x_29_Site_photographs_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site photographs and/or videos (optional)'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5b4ce68152e52'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_30_Site_photograph_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph')
    x_31_Site_video_x = models.FileField(upload_to='ec5/', verbose_name='Site video')

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
    x_32_Date_of_trapping_x = models.TextField(verbose_name='Date of trapping event')
    x_34_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event began (nets opened)')
    x_35_Date_traps_closed_x = models.TextField(verbose_name='Date traps closed (may extend a day)')
    x_36_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event ended (nets closed)')
    x_37_Weather_condition_x = models.TextField(verbose_name='Weather conditions during trapping event')
    x_39_Number_of_26_mete_x = models.IntegerField(verbose_name='Number of 2.6 meter nets', blank=True, null=True)
    x_40_Number_of_4_meter_x = models.IntegerField(verbose_name='Number of 4 meter nets', blank=True, null=True)
    x_41_Number_of_6_meter_x = models.IntegerField(verbose_name='Number of 6 meter nets', blank=True, null=True)
    x_42_Number_of_9_meter_x = models.IntegerField(verbose_name='Number of 9 meter nets', blank=True, null=True)
    x_43_Number_of_harp_tr_x = models.IntegerField(verbose_name='Number of harp traps', blank=True, null=True)
    x_45_Page_1_x = models.FileField(upload_to='ec5/', verbose_name='Page 1')
    x_46_Page_2_x = models.FileField(upload_to='ec5/', verbose_name='Page 2')
    x_47_Page_3_x = models.FileField(upload_to='ec5/', verbose_name='Page 3')
    x_48_Field_notes_x = models.TextField(verbose_name='Field notes')

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
    x_50_ANIMAL_ID_eg_PK00_x = models.TextField(verbose_name='ANIMAL ID        [eg. PK0001] ')
    x_51_Bat_family_x = models.TextField(verbose_name='Bat family')
    x_52_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat family')
    x_53_Family_Emballonur_x = models.TextField(verbose_name='Family: Emballonuridae')
    x_54_Family_Hipposider_x = models.TextField(verbose_name='Family: Hipposideridae')
    x_55_Family_Megadermat_x = models.TextField(verbose_name='Family: Megadermatidae')
    x_56_Family_Miniopteri_x = models.TextField(verbose_name='Family: Miniopteridae')
    x_57_Family_Molossidae_x = models.TextField(verbose_name='Family: Molossidae')
    x_58_Family_Nycteridae_x = models.TextField(verbose_name='Family: Nycteridae')
    x_59_Family_Pteropodid_x = models.TextField(verbose_name='Family: Pteropodidae')
    x_60_Family_Rhinolophi_x = models.TextField(verbose_name='Family: Rhinolophidae')
    x_61_Family_Rhinopomat_x = models.TextField(verbose_name='Family: Rhinopomatidae')
    x_62_Family_Vespertili_x = models.TextField(verbose_name='Family: Vespertilionidae')
    x_63_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat species')
    x_64_Age_x = models.TextField(verbose_name='Age')
    x_65_Sex_x = models.TextField(verbose_name='Sex')
    x_66_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Male')
    x_67_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Female')
    x_69_Forearm_length_mm_x = models.TextField(verbose_name='Forearm length (mm)')
    x_70_Body_mass_g_x = models.TextField(verbose_name='Body mass (g)')
    x_71_Ear_length_mm_x = models.TextField(verbose_name='Ear length (mm)')
    x_72_Tail_length_mm_x = models.TextField(verbose_name='Tail length (mm)')
    x_73_Foot_length_mm_x = models.TextField(verbose_name='Foot length (mm)')
    x_74_Head_body_length_x = models.TextField(verbose_name='Head & body length (mm)')
    x_75_Other_morphologic_x = models.TextField(verbose_name='Other morphological measurement taken')
    x_77_Picture_1_x = models.FileField(upload_to='ec5/', verbose_name='Picture 1')
    x_78_Picture_2_x = models.FileField(upload_to='ec5/', verbose_name='Picture 2')
    x_79_Video_1_x = models.FileField(upload_to='ec5/', verbose_name='Video 1')
    x_80_Video_2_x = models.FileField(upload_to='ec5/', verbose_name='Video 2')
    x_81_Collect_diagnosti_x = models.TextField(verbose_name='Collect diagnostic samples - swabs, urine/feces, blood?')
    x_82_Collect_ORAL_swab_x = models.TextField(verbose_name='Collect ORAL swabs?')
    x_84_Oral_swab_OS_stor_x = models.TextField(verbose_name='Oral swab (OS) stored in TRIZOL (T)')
    x_85_Oral_swab_OS_stor_x = models.TextField(verbose_name='Oral swab (OS) stored in RNAlater (R)')
    x_86_Collect_FECES_fre_x = models.TextField(verbose_name='Collect FECES (fresh) or RECTAL swabs?')
    x_88_FECES_stored_in_T_x = models.TextField(verbose_name='FECES stored in TRIZOL (T)')
    x_89_Rectal_swab_RS_st_x = models.TextField(verbose_name='Rectal swab (RS) stored in TRIZOL (T)')
    x_90_FECES_stored_in_R_x = models.TextField(verbose_name='FECES stored in RNAlater (R)')
    x_91_Rectal_swab_RS_st_x = models.TextField(verbose_name='Rectal swab (RS) stored in RNAlater (R)')
    x_92_Collect_URINE_UR_x = models.TextField(verbose_name='Collect URINE (UR) in RNALater?')
    x_93_Collect_BLOOD_x = models.TextField(verbose_name='Collect BLOOD?')
    x_95_Whole_blood_WB_st_x = models.TextField(verbose_name='Whole blood (WB) stored in TRIZOL (T)')
    x_96_Whole_blood_WB_st_x = models.TextField(verbose_name='Whole blood (WB) stored in RNAlater (R)')
    x_97_Estimate_microlit_x = models.TextField(verbose_name='Estimate microliters of blood drawn')
    x_98_Blood_plasma_BP_s_x = models.TextField(verbose_name='Blood plasma (BP) stored in RNAlater (R)')
    x_99_Prepare_BLOOD_SM_x = models.TextField(verbose_name='Prepare BLOOD - SMEAR?')
    x_100_Collect_WING_BIO_x = models.TextField(verbose_name='Collect WING BIOPSY PUNCH?')
    x_101_Collect_OTHER_sa_x = models.TextField(verbose_name='Collect OTHER samples (eg. ectoparasites)')
    x_102_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected')
    x_103_Acoustic_recordi_x = models.TextField(verbose_name='Acoustic recordings taken?')
    x_104_OTHER_samples_co_x = models.TextField(verbose_name='OTHER samples collected on included on the list')
    x_114_Necropsy_perform_x = models.TextField(verbose_name='Necropsy performed?')
    x_116_Date_necropsy_pe_x = models.TextField(verbose_name='Date necropsy performed')
    x_117_Person_performin_x = models.TextField(verbose_name='Person performing the necropsy')
    x_118_Samples_collecte_x = models.TextField(verbose_name='Samples collected during necropsy (store in RNAlater)')
    x_119_Bat_prepared_as_x = models.TextField(verbose_name='Bat prepared as museum specimen?')
    x_120_If_yes_deposited_x = models.TextField(verbose_name='If yes, deposited at what facility?')
    x_121_Additional_infor_x = models.TextField(verbose_name='Additional information noted')


class x_105_Acoustic_recordi_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Acoustic recording information'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456e7bf94bc_5b4ce74352e58'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(BatData, on_delete=models.CASCADE)
    x_106_Recording_equipm_x = models.TextField(verbose_name='Recording equipment used (if not Echo Meter Touch Pro 2)')
    x_107_Site_conditions_x = models.TextField(verbose_name='Site conditions where recording was taken')
    x_108_Specify_other_si_x = models.TextField(verbose_name='Specify other site conditions')
    x_109_Recording_method_x = models.TextField(verbose_name='Recording method')
    x_110_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 1')
    x_111_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 2')
    x_112_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 3')
    x_113_File_numbers_typ_x = models.TextField(verbose_name='File number(s), typically xxxx.wav')

