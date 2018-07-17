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
    x_7_Specify_Other_site_x = models.TextField(verbose_name='Specify "Other" site type:')
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
    x_26_Specify_Other_sit_x = models.TextField(verbose_name='Specify "Other" site modifications')
    x_27_Frequency_of_huma_x = models.TextField(verbose_name='Frequency of human visitation to the site')
    x_28_Evidence_of_human_x = models.TextField(verbose_name='Evidence of human disturbance at site (select all that apply)')
    x_29_Specify_Other_evi_x = models.TextField(verbose_name='Specify "Other" evidence of human disturbance at site')
    x_33_Voicerecorded_fie_x = models.FileField(upload_to='ec5/', verbose_name='Voice-recorded field notes (optional)')


class x_30_Site_photographs_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site photographs and/or videos (optional)'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5aeb50c6d334a_5b4ce68152e52'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_31_Site_photograph_x = models.FileField(upload_to='ec5/', verbose_name='Site photograph')
    x_32_Site_video_x = models.FileField(upload_to='ec5/', verbose_name='Site video')

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
    x_34_Date_of_trapping_x = models.TextField(verbose_name='Date of trapping event')
    x_36_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event began (nets opened)')
    x_37_Time_trapping_eve_x = models.TextField(verbose_name='Time trapping event ended (nets closed)')
    x_38_Weather_condition_x = models.TextField(verbose_name='Weather conditions during trapping event')
    x_40_Number_of_26_mete_x = models.IntegerField(verbose_name='Number of 2.6 meter nets', blank=True, null=True)
    x_41_Number_of_4_meter_x = models.IntegerField(verbose_name='Number of 4 meter nets', blank=True, null=True)
    x_42_Number_of_6_meter_x = models.IntegerField(verbose_name='Number of 6 meter nets', blank=True, null=True)
    x_43_Number_of_9_meter_x = models.IntegerField(verbose_name='Number of 9 meter nets', blank=True, null=True)
    x_44_Number_of_harp_tr_x = models.IntegerField(verbose_name='Number of harp traps', blank=True, null=True)

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
    x_46_ANIMAL_ID_eg_PK00_x = models.TextField(verbose_name='ANIMAL ID        [eg. PK0001] ')
    x_47_Bat_family_x = models.TextField(verbose_name='Bat family')
    x_48_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat family')
    x_49_Family_Emballonur_x = models.TextField(verbose_name='Family: Emballonuridae')
    x_50_Family_Hipposider_x = models.TextField(verbose_name='Family: Hipposideridae')
    x_51_Family_Megadermat_x = models.TextField(verbose_name='Family: Megadermatidae')
    x_52_Family_Miniopteri_x = models.TextField(verbose_name='Family: Miniopteridae')
    x_53_Family_Molossidae_x = models.TextField(verbose_name='Family: Molossidae')
    x_54_Family_Nycteridae_x = models.TextField(verbose_name='Family: Nycteridae')
    x_55_Family_Pteropodid_x = models.TextField(verbose_name='Family: Pteropodidae')
    x_56_Family_Rhinolophi_x = models.TextField(verbose_name='Family: Rhinolophidae')
    x_57_Family_Rhinopomat_x = models.TextField(verbose_name='Family: Rhinopomatidae')
    x_58_Family_Vespertili_x = models.TextField(verbose_name='Family: Vespertilionidae')
    x_59_Specify_Other_bat_x = models.TextField(verbose_name='Specify "Other" bat species')
    x_60_Age_x = models.TextField(verbose_name='Age')
    x_61_Sex_x = models.TextField(verbose_name='Sex')
    x_62_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Male')
    x_63_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Female')
    x_65_Forearm_length_mm_x = models.TextField(verbose_name='Forearm length (mm)')
    x_66_Body_mass_g_x = models.TextField(verbose_name='Body mass (g)')
    x_67_Ear_length_mm_x = models.TextField(verbose_name='Ear length (mm)')
    x_68_Tail_length_mm_x = models.TextField(verbose_name='Tail length (mm)')
    x_69_Foot_length_mm_x = models.TextField(verbose_name='Foot length (mm)')
    x_70_Total_length_mm_x = models.TextField(verbose_name='Total length (mm) - snout to tail tip')
    x_72_Picture_1_x = models.FileField(upload_to='ec5/', verbose_name='Picture 1')
    x_73_Picture_2_x = models.FileField(upload_to='ec5/', verbose_name='Picture 2')
    x_74_Video_x = models.FileField(upload_to='ec5/', verbose_name='Video')
    x_75_Collect_diagnosti_x = models.TextField(verbose_name='Collect diagnostic samples?')
    x_76_Collect_ORAL_swab_x = models.TextField(verbose_name='Collect ORAL swabs?')
    x_78_Oral_swab_stored_x = models.TextField(verbose_name='Oral swab stored in TRIZOL (T)')
    x_79_SAMPLE_ID_oral_s_x = models.TextField(verbose_name='SAMPLE ID - oral swab in Trizol [AnimalID.OST]')
    x_80_Oral_swab_stored_x = models.TextField(verbose_name='Oral swab stored in RNAlater (R)')
    x_81_SAMPLE_ID_oral_s_x = models.TextField(verbose_name='SAMPLE ID - oral swab in RNAlater [AnimalID.OSR]')
    x_82_Collect_RECTAL_sw_x = models.TextField(verbose_name='Collect RECTAL swabs?')
    x_84_Rectal_swab_store_x = models.TextField(verbose_name='Rectal swab stored in TRIZOL (T)')
    x_85_SAMPLE_ID_rectal_x = models.TextField(verbose_name='SAMPLE ID - rectal swab in Trizol [AnimalID.RST]')
    x_86_Rectal_swab_store_x = models.TextField(verbose_name='Rectal swab stored in RNAlater (R)')
    x_87_SAMPLE_ID_rectal_x = models.TextField(verbose_name='SAMPLE ID - rectal swab in RNAlater [AnimalID.RSR]')
    x_88_Collect_URINE_fre_x = models.TextField(verbose_name='Collect URINE (fresh)?')
    x_90_Urine_fresh_store_x = models.TextField(verbose_name='Urine (fresh) stored in TRIZOL (T)')
    x_91_SAMPLE_ID_urine_x = models.TextField(verbose_name='SAMPLE ID - urine in Trizol [AnimalID.URT]')
    x_92_Urine_fresh_store_x = models.TextField(verbose_name='Urine (fresh) stored in RNAlater (R)')
    x_93_SAMPLE_ID_urine_x = models.TextField(verbose_name='SAMPLE ID - urine in RNAlater [AnimalID.URR]')
    x_94_Collect_FECES_fre_x = models.TextField(verbose_name='Collect FECES (fresh)?')
    x_96_Feces_fresh_store_x = models.TextField(verbose_name='Feces (fresh) stored in TRIZOL (T)')
    x_97_SAMPLE_ID_feces_x = models.TextField(verbose_name='SAMPLE ID - feces in Trizol [AnimalID.FET]')
    x_98_Feces_fresh_store_x = models.TextField(verbose_name='Feces (fresh) stored in RNAlater (R)')
    x_99_SAMPLE_ID_feces_x = models.TextField(verbose_name='SAMPLE ID - feces in RNAlater [AnimalID.FER]')
    x_100_Collect_BLOOD_P_x = models.TextField(verbose_name='Collect BLOOD - PLASMA?')
    x_102_Plasma_stored_in_x = models.TextField(verbose_name='Plasma stored in TRIZOL (T)')
    x_103_SAMPLE_ID_plasm_x = models.TextField(verbose_name='SAMPLE ID - plasma in Trizol [AnimalID.BPT]')
    x_104_Plasma_stored_in_x = models.TextField(verbose_name='Plasma stored in RNAlater (R)')
    x_105_SAMPLE_ID_plasm_x = models.TextField(verbose_name='SAMPLE ID - plasma in RNAlater [AnimalID.BPR]')
    x_106_Prepare_BLOOD_S_x = models.TextField(verbose_name='Prepare BLOOD - SMEAR?')
    x_107_Collect_WING_BIO_x = models.TextField(verbose_name='Collect WING BIOPSY PUNCH?')
    x_108_Acoustic_recordi_x = models.TextField(verbose_name='Acoustic recordings taken?')
    x_112_Necropsy_perform_x = models.TextField(verbose_name='Necropsy performed?')
    x_114_Date_necropsy_pe_x = models.TextField(verbose_name='Date necropsy performed')
    x_115_Person_performin_x = models.TextField(verbose_name='Person performing the necropsy')
    x_116_Samples_collecte_x = models.TextField(verbose_name='Samples collected during necropsy (store in RNAlater)')
    x_117_Bat_prepared_as_x = models.TextField(verbose_name='Bat prepared as museum specimen?')
    x_118_If_yes_deposited_x = models.TextField(verbose_name='If yes, deposited at what facility?')


class x_109_Acoustic_recordi_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Acoustic recording information'
    ec5_is_branch = True
    ec5_ref = '0676a95106ee4c3594ea16975fdbe3ba_5b456e7bf94bc_5b4ce74352e58'
    id = models.CharField(max_length=100, primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(BatData, on_delete=models.CASCADE)
    x_110_Recording_method_x = models.TextField(verbose_name='Recording method')
    x_111_Acoustic_recordi_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording')

