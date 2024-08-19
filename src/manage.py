import sqlite3
import src.sqliteObjects as sqliteObjects
import pandas as pd

def importFromFile(file, db):
    contents = pd.DataFrame()

    # Read the file
    if file.filename.endswith(('xlsx', 'xls')):
        contents = pd.read_excel(file, dtype=object)
    elif file.filename.endswith('csv'):
        contents = pd.read_csv(file, dtype=object, low_memory=False, thousands=',', encoding='utf-16', sep='\t')
    
    columnMap = {
        "TRI Incident Number": "tri_incident_number",
        "TRI Interaction Number": "tri_interaction_number",
        "MOS Command Description": "mos_command_description",
        "MOS Rank Code": "mos_rank_code",
        "MOS Full Name": "mos_full_name",
        "MOS Tax Number": "mos_tax_number",
        "Occurrence Date": "occurrence_date",
        "Occurrence Time": "occurrence_time",
        "TRI_Interaction_Key" : "tri_interaction_key",
        "Create Timestamp": "create_timestamp",
        "Report Timestamp": "report_timestamp",
        "Effective Timestamp": "effective_timestamp",
        "TRI Level": "tri_level",
        "TRI Voided Flag": "tri_voided_flag",
        "Endorsement Timestamp": "endorsement_timestamp",
        "Encounter Type Description": "encounter_type_description",
        "Person Type Code": "person_type_code",
        "MOS Command Code": "mos_command_code",
        "BORO": "boro",
        "MOS TRI Role Description": "mos_tri_role_description",
        "Injury Sustained Flag": "injury_sustained_flag",
        "BWC Video Flag": "bwc_video_flag",
        "BWC Viewed Flag": "bwc_viewed_flag",
        "MOS On Duty Flag": "mos_on_duty_flag",
        "MOS In Uniform Flag": "mos_in_uniform_flag",
        "MOS Worn Camera Flag": "mos_worn_camera_flag",
        "Weapon Used Code": "weapon_used_code",
        "Action Prohibited by PG 221 01 Flag": "action_prohibited_by_pg_221_01_flag",
        "Alleged Suspected Excessive Force Flag": "alleged_suspected_excessive_force_flag",
        "FAM None Flag": "fam_none_flag",
        "FAM Hand Strike Flag": "fam_hand_strike_flag",
        "FAM Object Strike Flag": "fam_object_strike_flag",
        "FAM Foot Strike Flag": "fam_foot_strike_flag",
        "FAM Menacing Brandishing Weapon Flag": "fam_menacing_brandishing_weapon_flag",
        "FAM Object Thrown Flag": "fam_object_thrown_flag",
        "FAM Wrestling Grappling Flag": "fam_wrestling_grappling_flag",
        "FAM Assault with Knife Sharp Object Flag": "fam_assault_with_knife_sharp_object_flag",
        "FAM Discharged Firearm at Officer Flag": "fam_discharged_firearm_at_officer_flag",
        "FAM Pushing Shoving Flag": "fam_pushing_shoving_flag",
        "FAM MOS Self Inflicted Flag": "fam_mos_self_inflicted_flag",
        "FAM MOS Injured Attempting to Apprehend Control Subject Flag": "fam_mos_injured_attempting_to_apprehend_control_subject_flag",
        "FAM Bitten Flag": "fam_bitten_flag",
        "FAM Physical Harrassment Flag": "fam_physical_harrassment_flag",
        "FAM Active Resistance Flag": "fam_active_resistance_flag",
        "FAM Intentionally Spitting Bleeding Flag": "fam_intentionally_spitting_bleeding_flag",
        "i_FAM_Other_Flag": "i_fam_other_flag",
        "i_FAM_Other_Description": "i_fam_other_description",
        "i_ISM_Injury_Sustained_by_MOS_None_Flag": "i_ism_injury_sustained_by_mos_none_flag",
        "i_ISM_Minor_Swelling_Flag": "i_ism_minor_swelling_flag",
        "i_ISM_Contusions_Flag": "i_ism_contusions_flag",
        "i_ISM_Significant_Contusions_Flag": "i_ism_significant_contusions_flag",
        "i_ISM_Complaint_of_Substantial_Pain_Flag": "i_ism_complaint_of_substantial_pain_flag",
        "i_ISM_Lacerations_requiring_sutures_Flag": "i_ism_lacerations_requiring_sutures_flag",
        "i_ISM_Broken_Fractured_Bones_Flag": "i_ism_broken_fractured_bones_flag",
        "i_ISM_Gunshot_Wound_Flag": "i_ism_gunshot_wound_flag",
        "i_ISM_Heart_Attack_Stroke_Aneurysm_Flag": "i_ism_heart_attack_stroke_aneurysm_flag",
        "i_ISM_Killed_Flag": "i_ism_killed_flag",
        "i_ISM_Burn_Flag": "i_ism_burn_flag",
        "i_ISM_Canine_Bite_Flag": "i_ism_canine_bite_flag",
        "i_ISM_Possible_Internal_Injury_Flag": "i_ism_possible_internal_injury_flag",
        "i_ISM_Loss_of_Body_Part_Flag": "i_ism_loss_of_body_part_flag",
        "i_ISM_Sprain_Strain_Flag": "i_ism_sprain_strain_flag",
        "i_ISM_Loss_Of_Tooth_Teeth_Flag": "i_ism_loss_of_tooth_teeth_flag",
        "i_ISM_Unconsciousness_Flag": "i_ism_unconscousness_flag",
        "i_ISM_Abrasions_Lacerations_Flag": "i_ism_abrasions_lacerations_flag",
        "i_ISM_Other_Condition_Injury_Flag": "i_ism_other_condition_injury_flag",
        "i_ISM_Other_Condition_Injury_Description": "i_ism_other_condition_injury_description",
        "RMF Not Applicable Flag": "rmf_not_applicable_flag",
        "RMF Defense of self Flag": "rmf_defense_of_self_flag",
        "RMF Defense of Other MOS Flag": "rmf_defense_of_other_mos_flag",
        "RMF Defense of Member of Public Flag": "rmf_defense_of_member_of_public_flag",
        "RMF Stop Self Inflicted Harm Flag": "rmf_stop_self_inflicted_harm_flag",
        "RMF Fleeing Suspect Flag": "rmf_fleeing_suspect_flag",
        "RMF Overcome Resistance or Aggresion Flag": "rmf_overcome_resistance_or_aggresion_flag",
        "RMF Subject Armed with Weapon Flag": "rmf_subject_armed_with_weapon_flag",
        "RMF Unintentional Flag": "rmf_unintentional_flag",
        "FMT No Force Used": "fmt_no_force_used",
        "FMT Conducted Electrical Weapon Drive Stun Flag": "fmt_conducted_electrical_weapon_drive_stun_flag",
        "FMT Conducted Electrical Weapon Probes Flag": "fmt_conducted_electrical_weapon_probes_flag",
        "FMT Hand Strike Flag": "fmt_hand_strike_flag",
        "FMT Foot Strike Flag": "fmt_foot_strike_flag",
        "FMT Forcible Take Down": "fmt_forcible_take_down",
        "FMT OC Spray Flag": "fmt_oc_spray_flag",
        "FMT Restraining Mesh Blanket Flag": "fmt_restraining_mesh_blanket_flag",
        "FMT Impact Weapon Flag": "fmt_impact_weapon_flag",
        "FMT Police Canine Bite Flag": "fmt_police_canine_bite_flag",
        "FMT Discharged Firearm Flag": "fmt_discharged_firearm_flag",
        "FMT Intentionally Struck Subject With Vehicle Flag": "fmt_intentionally_struck_subject_with_vehicle_flag",
        "FMT Wrestling Grappling Flag": "fmt_wrestling_grappling_flag",
        "FMT Other Force Flag": "fmt_other_force_flag",
        "FMT Other Force Desc": "fmt_other_force_desc",
        "Person_Type_Code": "person_type_code",
        "Role_Description": "role_description",
        "Person_Full_Name": "person_full_name",
        "Subject_Injured_Flag": "subject_injured_flag",
        "Subject_Resisted_Flag": "subject_resisted_flag",
        "Subject_Used_Force_Flag": "subject_used_force_flag",
        "Medical_Attention_Needed": "medical_attention_needed",
        "EMS_Treated_Description": "ems_treated_description",
        "Summons_Issued_Flag": "summons_issued_flag",
        "Arrest_Made_Flag": "arrest_made_flag",
        "Arrest_Number": "arrest_number",
        "Top_Charge": "top_charge",
        "i_CSI_No_Injury_Flag": "i_csi_no_injury_flag",
        "i_CSI_Broken_Fractured_Bones_Flag": "i_csi_broken_fractured_bones_flag",
        "i_CSI_Complaint_of_Substential_Pain_Flag": "i_csi_complaint_of_substential_pain_flag",
        "i_CSI_Gunshot_Wound_Flag": "i_csi_gunshot_wound_flag",
        "i_CSI_Heart_Attack_Stroke_Aneurysm_Flag": "i_csi_heart_attack_stroke_aneurysm_flag",
        "i_CSI_Lacerations_Requiring_Stitches_Staples_Flag": "i_csi_lacerations_requiring_stitches_staples_flag",
        "i_CSI_Loss_Of_Tooth_Teeth_Flag": "i_csi_loss_of_tooth_teeth_flag",
        "i_CSI_Minor_Contusions_Flag": "i_csi_minor_contusions_flag",
        "i_CSI_Minor_Lacerations_Abrasion_Flag": "i_csi_minor_lacerations_abrasion_flag",
        "i_CSI_Minor_Swelling_Flag": "i_csi_minor_swelling_flag",
        "i_CSI_Subject_Civilian_Bystander_Died_Flag": "i_csi_subject_civilian_bystander_died_flag",
        "i_CSI_Subject_Civilian_Bystander_Likely_to_Die_Flag": "i_csi_subject_civilian_bystander_likely_to_die_flag",
        "i_CSI_Unconsciousness_Flag": "i_csi_unconsciousness_flag",
        "i_CSI_Unknown_Flag": "i_csi_unknown_flag",
        "i_CSI_Other_Condition_Requiring_Hospital_Admission_Flag": "i_csi_other_condition_requiring_hospital_admission_flag",
        "i_CSI_Other_Condition_Description": "i_csi_other_condition_description",
        "ISM YES Flag": "ism_yes_flag",
        "DB_Category": "db_category"
    }

    # Renames the columns
    contents = contents.rename(columns=columnMap)

    # Drop the entry columns if they are present
    columnsToDrop = ['BWC COMMAND (Y/N)','BWC USER AT TIME OF INCIDENT (Y/N)','VIDEO OF FORCE INCIDENT (Y/N)','FORCE INCIDENT EVIDENCE SERIAL NUMBER','LATE ACTIVATION? (Y/N)',
    'EARLY DEACTIVATION? (Y/N)','SHARED WITH ADA? (Y/N)','VIDEO CATEGORIZED AS FORCE INCIDENT (Y/N)','TRI NUMBER ENTERED IN METADATA (Y/N)',
    'MULTIPLE VIDEOS OF INCIDENT BY USER (Y/N)','ALL EVIDENCE SERIAL NUMBERS']

    for column in columnsToDrop:
        if column in contents.columns:
                contents = contents.drop(columns=column)

    # Increment the index by 1 so it doesnt start from 0
    contents.index += 1

    conn = db.connect()

    # Send the dataframe to sql
    try:
        contents.to_sql('interactions', conn, if_exists='append', index=True)
    except:
        pass
    
    conn.commit()
    conn.close()

    return