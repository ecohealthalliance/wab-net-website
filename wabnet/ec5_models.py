# These models were generated from the Epicollect 5 project via generate_models.py
from django.db import models
from . import entity_keywords_model
from django.contrib.contenttypes.fields import GenericRelation

project_name = 'nathan-test-wabnet3'

class SiteData(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'field_data_forms'
    ec5_is_branch = False
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970'
    uuid = models.CharField(max_length=100, primary_key=True)
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    country = models.TextField(verbose_name='Country')
    x_3_Site_name_x = models.TextField(verbose_name='Site name')
    x_4_Site_location_GPS_x = models.TextField(verbose_name='Site location (GPS coords.)')
    x_34_Weather_condition_x = models.TextField(verbose_name='Weather conditions prior to and during trapping?')
    x_35_Time_trapping_beg_x = models.TextField(verbose_name='Time trapping began (nets open)?')
    x_36_Time_trapping_end_x = models.TextField(verbose_name='Time trapping ended (nets closed)?')
    x_37_Number_of_26_mete_x = models.TextField(verbose_name='Number of 2.6 meter nets?')
    x_38_Number_of_4_meter_x = models.TextField(verbose_name='Number of 4 meter nets?')
    x_39_Number_of_6_meter_x = models.TextField(verbose_name='Number of 6 meter nets?')
    x_40_Number_of_9_meter_x = models.TextField(verbose_name='Number of 9 meter nets?')
    x_41_Number_of_12_mete_x = models.TextField(verbose_name='Number of 12 meter nets?')
    x_42_Number_of_harp_tr_x = models.TextField(verbose_name='Number of harp traps?')


class x_5_Site_characterizat_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Site characterization '
    ec5_is_branch = True
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970_5aeb5a485aa2c'
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_6_Date_of_site_chara_x = models.TextField(verbose_name='Date of site characterization')
    x_7_Site_type_x = models.TextField(verbose_name='Site type')
    x_8_Specify_other_site_x = models.TextField(verbose_name='Specify "other" site type')
    x_9_Guano_present_at_s_x = models.TextField(verbose_name='Guano present at site?')
    x_10_Estimated_human_p_x = models.TextField(verbose_name='Estimated human population size at site')
    x_11_Bathuman_interfac_x = models.TextField(verbose_name='Bat-human interface (check all that apply)')
    x_12_If_natural_area_w_x = models.TextField(verbose_name='If natural area, what setting?')
    x_13_If_forest_what_is_x = models.TextField(verbose_name='If forest, what is the estimated area?')
    x_14_If_forest_what_co_x = models.TextField(verbose_name='If forest, what condition is the forest?')
    x_15_If_cave_what_is_t_x = models.TextField(verbose_name='If cave, what is the estimated length of the cave?')
    x_16_If_cave_what_is_t_x = models.TextField(verbose_name='If cave, what is the structural heterogeneity of the cave?')
    x_17_Other_wildlife_sp_x = models.TextField(verbose_name='Other wildlife species observed at the site?')
    x_18_List_other_wildli_x = models.TextField(verbose_name='List other wildlife observed, be specific.')
    x_19_Domestic_animals_x = models.TextField(verbose_name='Domestic animals observed at the site?')
    x_20_List_domestic_ani_x = models.TextField(verbose_name='List domestic animals observed, be specific.')
    x_21_Is_water_present_x = models.TextField(verbose_name='Is water present at the site?')
    x_22_Is_water_shared_b_x = models.TextField(verbose_name='Is water shared between animals/wildlife and humans?')
    x_23_Site_accessibilit_x = models.TextField(verbose_name='Site accessibility')
    x_24_Site_accommodatio_x = models.TextField(verbose_name='Site accommodations for humans')
    x_25_Other_accommodati_x = models.TextField(verbose_name='Other accommodations observed, but not listed above')
    x_26_Frequency_of_huma_x = models.TextField(verbose_name='Frequency of human visitation to the site')
    x_27_Evidence_of_distu_x = models.TextField(verbose_name='Evidence of disturbance (select all that apply)')
    x_28_Other_evidence_of_x = models.TextField(verbose_name='Other evidence of disturbance, but not listed above')
    x_29_Observed_in_1_km_x = models.TextField(verbose_name='Observed in 1 km radius of site')
    x_30_Other_structures_x = models.TextField(verbose_name='Other structures observed in 1 km radius, but not listed above')
    x_31_Site_photographs_x = models.FileField(upload_to='ec5/', verbose_name='Site photographs')
    x_32_Site_video_x = models.FileField(upload_to='ec5/', verbose_name='Site video')


class BatCaptureData(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Bat capture data'
    ec5_is_branch = True
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970_5aeb5ab65aa2e'
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_44_Unique_ANIMAL_ID_x = models.TextField(verbose_name='Unique ANIMAL ID number')
    x_45_Family_x = models.TextField(verbose_name='Family')
    x_46_Family_Emballonur_x = models.TextField(verbose_name='Family: Emballonuridae')
    x_47_Family_Hipposider_x = models.TextField(verbose_name='Family: Hipposideridae')
    x_48_Family_Megadermat_x = models.TextField(verbose_name='Family: Megadermatidae')
    x_49_Family_Miniopteri_x = models.TextField(verbose_name='Family: Miniopteridae')
    x_50_Family_Molossidae_x = models.TextField(verbose_name='Family: Molossidae')
    x_51_Family_Nycteridae_x = models.TextField(verbose_name='Family: Nycteridae')
    x_52_Family_Pteropodid_x = models.TextField(verbose_name='Family: Pteropodidae')
    x_53_Family_Rhinolophi_x = models.TextField(verbose_name='Family: Rhinolophidae')
    x_54_Family_Rhinopomat_x = models.TextField(verbose_name='Family: Rhinopomatidae')
    x_55_Family_Vespertili_x = models.TextField(verbose_name='Family: Vespertilionidae')
    x_56_Age_x = models.TextField(verbose_name='Age')
    x_57_Sex_x = models.TextField(verbose_name='Sex')
    x_58_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Male')
    x_59_Reproductive_stat_x = models.TextField(verbose_name='Reproductive status: Female')
    x_61_Forearm_length_mi_x = models.TextField(verbose_name='Forearm length (millimeters)')
    x_62_Body_mass_grams_x = models.TextField(verbose_name='Body mass (grams)')
    x_63_Ear_length_millim_x = models.TextField(verbose_name='Ear length (millimeters) - optional')
    x_64_Foot_length_milli_x = models.TextField(verbose_name='Foot length (millimeters) - optional')
    x_65_Tail_length_milli_x = models.TextField(verbose_name='Tail length (millimeters) - optional')
    x_66_Body_and_head_len_x = models.TextField(verbose_name='Body and head length (millimeters) - optional')
    x_67_Picture_of_captur_x = models.FileField(upload_to='ec5/', verbose_name='Picture of captured bat')
    x_68_Video_optional_x = models.FileField(upload_to='ec5/', verbose_name='Video (optional)')
    x_69_Oral_swab_x = models.TextField(verbose_name='Oral swab')
    x_71_Unique_SAMPLE_ID_x = models.TextField(verbose_name='Unique SAMPLE ID - oral swab in TRIzol')
    x_72_Unique_SAMPLE_ID_x = models.TextField(verbose_name='Unique SAMPLE ID - oral swab in RNAlater')
    x_73_Rectal_swab_x = models.TextField(verbose_name='Rectal swab')
    x_74_Unique_SAMPLE_ID_x = models.TextField(verbose_name='Unique SAMPLE ID number - rectal swabs in TRIzol')
    x_75_Unique_SAMPLE_ID_x = models.TextField(verbose_name='Unique SAMPLE ID number - rectal swabs in RNAlater')
    x_76_Feces_fresh_x = models.TextField(verbose_name='Feces - fresh')
    x_77_Urogenital_swab_x = models.TextField(verbose_name='Urogenital swab')
    x_78_Urine_fresh_x = models.TextField(verbose_name='Urine - fresh')
    x_79_Plasma_x = models.TextField(verbose_name='Plasma')
    x_80_Wing_biopsy_punch_x = models.TextField(verbose_name='Wing biopsy punch')
    x_81_Additional_inform_x = models.TextField(verbose_name='Additional information')


class x_82_Bat_acoustic_data_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Bat acoustic data'
    ec5_is_branch = True
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970_5af087872284e'
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_83_Unique_ANIMAL_ID_x = models.TextField(verbose_name='Unique ANIMAL ID number')
    x_84_Recording_method_x = models.TextField(verbose_name='Recording method')
    x_85_Acoustic_recordin_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 1')
    x_86_Acoustic_recordin_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 2')
    x_87_Acoustic_recordin_x = models.FileField(upload_to='ec5/', verbose_name='Acoustic recording 3')
    x_88_Start_frequency_k_x = models.TextField(verbose_name='Start frequency (kHz)')
    x_89_End_frequency_kHz_x = models.TextField(verbose_name='End frequency (kHz)')
    x_90_Peak_frequency_Fm_x = models.TextField(verbose_name='Peak frequency (Fmax)')
    x_91_Call_duration_mil_x = models.TextField(verbose_name='Call duration (milliseconds)')
    x_92_Bandwidth_x = models.TextField(verbose_name='Bandwidth')


class x_93_Bat_necropsy_form_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Bat necropsy form'
    ec5_is_branch = True
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970_5af0878a2284f'
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_94_Date_of_necropsy_x = models.TextField(verbose_name='Date of necropsy')
    x_95_Unique_ANIMAL_ID_x = models.TextField(verbose_name='Unique ANIMAL ID number')
    x_96_Samples_taken_sel_x = models.TextField(verbose_name='Samples taken (select all that apply)')
    x_97_Necropsy_photo_1_x = models.FileField(upload_to='ec5/', verbose_name='Necropsy photo 1')
    x_98_Necropsy_photo_2_x = models.FileField(upload_to='ec5/', verbose_name='Necropsy photo 2')
    x_99_Necropsy_photo_3_x = models.FileField(upload_to='ec5/', verbose_name='Necropsy photo 3')


class x_100_Lab_results_data_x(models.Model):
    keywords = GenericRelation(entity_keywords_model.EntityKeywords)
    name = 'Lab results data'
    ec5_is_branch = True
    ec5_ref = '92241edac9a74ee4afc7df55edf6beda_5b3f8dac25970_5aeb619e9a9eb'
    created_at = models.TextField()
    created_by = models.TextField()
    title = models.TextField()
    parent = models.ForeignKey(SiteData, on_delete=models.CASCADE)
    x_101_Unique_BAT_ID_x = models.TextField(verbose_name='Unique BAT ID')
    x_102_Unique_SAMPLE_ID_x = models.TextField(verbose_name='Unique SAMPLE ID: format AnimalID.SampleTypeSample#')
    x_103_Date_sample_coll_x = models.TextField(verbose_name='Date sample collected')
    x_104_Sample_type_x = models.TextField(verbose_name='Sample type')
    x_105_Sample_storage_m_x = models.TextField(verbose_name='Sample storage medium')
    x_106_Storage_facility_x = models.TextField(verbose_name='Storage facility')
    x_107_General_notes_ab_x = models.TextField(verbose_name='General notes about sample ')
    x_108_Test_date_x = models.TextField(verbose_name='Test date')
    x_109_Regional_lab_per_x = models.TextField(verbose_name='Regional lab performing sample testing')
    x_110_Test_type_x = models.TextField(verbose_name='Test type')