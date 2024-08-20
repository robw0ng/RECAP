# Imports
from flask import Flask, request, render_template, redirect, make_response
from flaskwebgui import FlaskUI

import pandas as pd
import json

import sys
import os
import io
import re

import src.sqliteObjects as sqlO
import src.manage as manageDB

from datetime import datetime

if getattr(sys, 'frozen', False): # This imports the splash screen library when used by pyinstaller
    import pyi_splash

if getattr(sys, 'frozen', False): # Closes the splash screen when used with py installer
    pyi_splash.close()

app = Flask(__name__)

db = sqlO.SQLiteDB('database/bwcDB.db') # Connects to the database

# Connecting to tables in the database
entries = db.getTable("entries") 
entriesMASTER = db.getTable('entriesMASTER')

interactions = db.getTable('interactions')
interactionMASTER = db.getTable('interactionsMASTER')

# Empty interaction dictionary to use when there is an entry without interaction displayed
emptyInteraction = {
    'tri_interaction_key': 0,
    'tri_incident_number': None,
    'tri_interaction_number': None,
    'mos_command_description': None,
    'mos_rank_code': None,
    'mos_full_name': None,
    'mos_tax_number': None,
    'occurrence_date': None,
    'occurrence_time': None,
    'create_timestamp': None,
    'report_timestamp': None,
    'effective_timestamp': None,
    'tri_level': None,
    'tri_voided_flag': None,
    'endorsement_timestamp': None,
    'encounter_type_description': None,
    'person_type_code': None,
    'mos_command_code': None,
    'boro': None,
    'mos_tri_role_description': None,
    'injury_sustained_flag': None,
    'bwc_video_flag': None,
    'bwc_viewed_flag': None,
    'mos_on_duty_flag': None,
    'mos_in_uniform_flag': None,
    'mos_worn_camera_flag': None,
    'weapon_used_code': None,
    'action_prohibited_by_pg_221_01_flag': None,
    'alleged_suspected_excessive_force_flag': None,
    'fam_none_flag': None,
    'fam_hand_strike_flag': None,
    'fam_object_strike_flag': None,
    'fam_foot_strike_flag': None,
    'fam_menacing_brandishing_weapon_flag': None,
    'fam_object_thrown_flag': None,
    'fam_wrestling_grappling_flag': None,
    'fam_assault_with_knife_sharp_object_flag': None,
    'fam_discharged_firearm_at_officer_flag': None,
    'fam_pushing_shoving_flag': None,
    'fam_mos_self_inflicted_flag': None,
    'fam_mos_injured_attempting_to_apprehend_control_subject_flag': None,
    'fam_bitten_flag': None,
    'fam_physical_harrassment_flag': None,
    'fam_active_resistance_flag': None,
    'fam_intentionally_spitting_bleeding_flag': None,
    'i_fam_other_flag': None,
    'i_fam_other_description': None,
    'i_ism_injury_sustained_by_mos_none_flag': None,
    'i_ism_minor_swelling_flag': None,
    'i_ism_contusions_flag': None,
    'i_ism_significant_contusions_flag': None,
    'i_ism_complaint_of_substantial_pain_flag': None,
    'i_ism_lacerations_requiring_sutures_flag': None,
    'i_ism_broken_fractured_bones_flag': None,
    'i_ism_gunshot_wound_flag': None,
    'i_ism_heart_attack_stroke_aneurysm_flag': None,
    'i_ism_killed_flag': None,
    'i_ism_burn_flag': None,
    'i_ism_canine_bite_flag': None,
    'i_ism_possible_internal_injury_flag': None,
    'i_ism_loss_of_body_part_flag': None,
    'i_ism_sprain_strain_flag': None,
    'i_ism_loss_of_tooth_teeth_flag': None,
    'i_ism_unconscousness_flag': None,
    'i_ism_abrasions_lacerations_flag': None,
    'i_ism_other_condition_injury_flag': None,
    'i_ism_other_condition_injury_description': None,
    'rmf_not_applicable_flag': None,
    'rmf_defense_of_self_flag': None,
    'rmf_defense_of_other_mos_flag': None,
    'rmf_defense_of_member_of_public_flag': None,
    'rmf_stop_self_inflicted_harm_flag': None,
    'rmf_fleeing_suspect_flag': None,
    'rmf_overcome_resistance_or_aggresion_flag': None,
    'rmf_subject_armed_with_weapon_flag': None,
    'rmf_unintentional_flag': None,
    'fmt_no_force_used': None,
    'fmt_conducted_electrical_weapon_drive_stun_flag': None,
    'fmt_conducted_electrical_weapon_probes_flag': None,
    'fmt_hand_strike_flag': None,
    'fmt_foot_strike_flag': None,
    'fmt_forcible_take_down': None,
    'fmt_oc_spray_flag': None,
    'fmt_restraining_mesh_blanket_flag': None,
    'fmt_impact_weapon_flag': None,
    'fmt_police_canine_bite_flag': None,
    'fmt_discharged_firearm_flag': None,
    'fmt_intentionally_struck_subject_with_vehicle_flag': None,
    'fmt_wrestling_grappling_flag': None,
    'fmt_other_force_flag': None,
    'fmt_other_force_desc': None,
    'role_description': None,
    'person_full_name': None,
    'subject_injured_flag': None,
    'subject_resisted_flag': None,
    'subject_used_force_flag': None,
    'medical_attention_needed': None,
    'ems_treated_description': None,
    'summons_issued_flag': None,
    'arrest_made_flag': None,
    'arrest_number': None,
    'top_charge': None,
    'i_csi_no_injury_flag': None,
    'i_csi_broken_fractured_bones_flag': None,
    'i_csi_complaint_of_substential_pain_flag': None,
    'i_csi_gunshot_wound_flag': None,
    'i_csi_heart_attack_stroke_aneurysm_flag': None,
    'i_csi_lacerations_requiring_stitches_staples_flag': None,
    'i_csi_loss_of_tooth_teeth_flag': None,
    'i_csi_minor_contusions_flag': None,
    'i_csi_minor_lacerations_abrasion_flag': None,
    'i_csi_minor_swelling_flag': None,
    'i_csi_subject_civilian_bystander_died_flag': None,
    'i_csi_subject_civilian_bystander_likely_to_die_flag': None,
    'i_csi_unconsciousness_flag': None,
    'i_csi_unknown_flag': None,
    'i_csi_other_condition_requiring_hospital_admission_flag': None,
    'i_csi_other_condition_description': None,
    'ism_yes_flag': None,
    'db_category': None
}

# This changes the icon for the app.
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# This function is used to convert the headers to snake case so that they can be referenced to the db and searched
def to_snake_case(string):
    string = re.sub(r"([A-Z]+)([A-Z][a-z\d])", r"\1_\2", string)
    string = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", string)
    string = string.replace("-", "_").replace(" ", "_").lower()
    return string

# Submits an entry by deleting any previous for the same interaction and inserting the entry in its place
def submit_entry(table, entry):
    table.delete(f"tri_interaction_key = {entry['tri_interaction_key']}")
    table.insert(entry)

# AJAX source for the entries tables
@app.route('/api/entries')
def entriesData():
    # Gets the entries as a list of dictionaries
    rowdictList = entries.getAllRowsAsDict()

    # Sort the list of dictionaries by the index
    rowdictList = sorted(rowdictList, key=lambda x: x['tri_index'])

    # Grab the search values in from the arguments passed through the api
    search = request.args.get('search[value]')
    colSearch = request.args.get('searchTerms')

    # First filter the dictionary list be checking if the search term is within the entire row
    if search:
        rowdictList = [row for row in rowdictList if search.lower() in str(row).lower()]
    
    # Then for every item in the column search dictionary, compare it with every column's values
    if colSearch:
        colSearchDict = json.loads(colSearch)
        for item in colSearchDict:
            rowdictList = [row for row in rowdictList if colSearchDict[item].lower() in str(row[to_snake_case(item)]).lower()]

    # This is the total length of filtered items
    total_filtered = len(rowdictList)

    # This is the range to display if there is nothing shown
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    rowdictList = rowdictList[start:start + length]

    return {
        'data': rowdictList,
        'recordsFiltered': total_filtered,
        'recordsTotal': (len(entries.getAllRowsAsDict())),
        'draw': request.args.get('draw', type=int),
    }

# AJAX source for the table that shows both entries and interactions on one row
@app.route('/api/entries_interactions')
def entriesInteractionsData():
    # Gets a list of dictionaries for the interactions
    interactionsDict = interactions.getAllRowsAsDict()
    # Same for the entries
    entriesDict = entries.getAllRowsAsDict()

    # Creates a list of only the interaction keys to make it easier to look them up
    interactionLookup = {interaction["tri_interaction_key"]: interaction for interaction in interactionsDict}

    combinedDict = []
    entriesWithoutInteraction = []

    # Iterates through the list of entries and it creates a new list of dictionaries combining the corresponding interaction
    # Additionally creates a list of entries with blank interactions as they dont have an entry that corresponds to it
    for entry in entriesDict:
        key = entry["tri_interaction_key"]
        if key in interactionLookup:
            combinedDict.append(interactionLookup[key] | entry)
        else:
            entriesWithoutInteraction.append(emptyInteraction | entry)

    # Combine the dicts to make one final dictionary that contains all entries with and without corresponding interactions
    finalDictList = combinedDict + entriesWithoutInteraction

    rowdictList = finalDictList
    # Sort the list of dictionaries by their index
    rowdictList = sorted(rowdictList, key=lambda x: x['index'])

    # Gets the search values
    search = request.args.get('search[value]')
    colSearch = request.args.get('searchTerms')

    # Gets the range to show
    viewRange = request.args.get('view')

    # The range is initially the length of the entire table
    iRange = [1,len(rowdictList)]

    # If the view range is specified, change the values in the IRange array to specify what bounds to show
    if viewRange:
        viewRangeDict = json.loads(viewRange)
        if viewRangeDict:
            if ("Start" in viewRangeDict.keys()):
                if viewRangeDict["Start"].isnumeric():
                    iRange[0] = int(viewRangeDict["Start"])

            if ("End" in viewRangeDict.keys()):
                if viewRangeDict["End"].isnumeric():
                    iRange[1] = int(viewRangeDict["End"])

    # Slices the start and end of the range to show
    rowdictList = rowdictList[iRange[0]-1 : iRange[1]]

    # If search filters present, search the entire row or the corresponding column
    if search:
        rowdictList = [row for row in rowdictList if search.lower() in str(row).lower()]
    
    if colSearch:
        colSearchDict = json.loads(colSearch)
        if colSearchDict:
            for item in colSearchDict:
                rowdictList = [row for row in rowdictList if colSearchDict[item].lower() in str(row[to_snake_case(item)]).lower()]

    # The amount of rows filtered from the total
    total_filtered = len(rowdictList)

    # Start and length data from ajax
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    rowdictList = rowdictList[start:start + length]

    return {
        'data': rowdictList,
        'recordsFiltered': total_filtered,
        'recordsTotal': (len(finalDictList)),
        'draw': request.args.get('draw', type=int),
    }

# AJAX source for the interactions
@app.route('/api/interactions')
def interactionsData():
    # Get the interactions as a list of dictionaries
    rowdictList = interactions.getAllRowsAsDict()
    # Sort the interactions by their index
    rowdictList = sorted(rowdictList, key=lambda x: x['index'])

    # Get the search filters
    search = request.args.get('search[value]')
    colSearch = request.args.get('searchTerms')

    # Get the range to show
    viewRange = request.args.get('view')

    # Get variable to show only incompleted entries
    incomplete = request.args.get('incomplete')

    # Intial range to display in the table (the full list)
    iRange = [1,len(rowdictList)]

    # If the view range is specified, set the corresponding items in the list to control what is displayed
    if viewRange:
        viewRangeDict = json.loads(viewRange)
        if viewRangeDict:
            if ("Start" in viewRangeDict.keys()):
                if viewRangeDict["Start"].isnumeric():
                    iRange[0] = int(viewRangeDict["Start"])

            if ("End" in viewRangeDict.keys()):
                if viewRangeDict["End"].isnumeric():
                    iRange[1] = int(viewRangeDict["End"])

    # Slices the list using the iRange values
    rowdictList = rowdictList[iRange[0]-1 : iRange[1]]

    # If search filters are present, search the whole row or respective columns
    if search:
        rowdictList = [row for row in rowdictList if search.lower() in str(row).lower()]

    if colSearch:
        colSearchDict = json.loads(colSearch)
        if colSearchDict:
            for item in colSearchDict:
                rowdictList = [row for row in rowdictList if colSearchDict[item].lower() in str(row[to_snake_case(item)]).lower()]

    # If incomplete only is checked, display entries that have not been submitted yet
    if incomplete:
        incompleteLoaded = json.loads(incomplete)
        if incompleteLoaded == True:
            rowdictList = [row for row in rowdictList if 'NO' in row['completed']]

    # Rest of the AJAX arguments
    total_filtered = len(rowdictList)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    rowdictList = rowdictList[start:start + length]

    return {
        'data': rowdictList,
        'recordsFiltered': total_filtered,
        'recordsTotal': (len(interactions.getAllRowsAsDict())),
        'draw': request.args.get('draw', type=int),
    }

# Entry page
@app.route('/')
def index():
    entriesRows = entries.getAllRowsAsDict()
    entriesRowsJSON = json.dumps(entriesRows) # Sends a JSON for the entry form to be filled out with

    return render_template(
                            'entry.html', 
                            entriesRowsJSON = entriesRowsJSON
                           )

# Submitting entries
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        # Gets the time for the submission time
        now = datetime.now()
        nowStr = now.strftime("%m/%d/%Y %H:%M:%S")
        # Saves the interaction key for use
        currentTri = request.form.get('intKey', None)

        # Creates the entry by getting the info from the form
        entry = {
            'entry_key' : None, 
            'tri_index' : request.form.get('interactionIndex', None),
            'tri_interaction_key' : currentTri, 
            "tri_incident_number": request.form.get('incNum', None),
            "tri_interaction_number": request.form.get('intNum', None),
            'user' : os.getlogin(),
            'reviewed' : 'NO',
            'video_of_force_incident' : request.form.get('VIDEO OF FORCE INCIDENT', None), 
            'good' : request.form.get('GOOD', None), 
            'bwc_command' : request.form.get('BWC COMMAND', None), 
            'bwc_user_at_time_of_incident' : request.form.get('BWC USER AT TIME OF INCIDENT', None), 
            'force_incident_serial_number' : request.form.get('fiSerial', None), 
            'force_incident_link' : request.form.get('fiLink', None), 
            'late_activation' : request.form.get('LATE ACTIVATION', None), 
            'early_deactivation' : request.form.get('EARLY DEACTIVATION', None), 
            'shared_with_ada' : request.form.get('SHARED WITH ADA', None), 
            'video_categorized_as_force_incident' : request.form.get('VIDEO CATEGORIZED AS FORCE INCIDENT', None), 
            'tri_number_entered_in_metadata' : request.form.get('TRI NUMBER ENTERED IN METADATA', None), 
            'multiple_videos_incident_by_user' : request.form.get('MULTIPLE VIDEOS OF INCIDENT BY USER', None), 
            'all_evidence_serial_numbers' : request.form.get('allSerial', None), 
            'all_evidence_links' : request.form.get('allLink', None),
            'dt_created' : nowStr,
            'dt_committed' : None
        }
        
        # If there is a TRI selected, submit the entry and update the interaction
        if currentTri != '':
            formInput = list(entry.values())[3:]
            if not (all((v == None or v == '') for v in formInput)):
                submit_entry(entries, entry)
                interactions.update( {'completed' : 'YES'}, f'tri_interaction_key = {currentTri}' )

    return redirect(request.referrer)

# Review page
@app.route('/review')
def review():
    entriesRowsJSON = json.dumps(entries.getAllRowsAsDict())

    return render_template(
                            'review.html',
                            entriesRowsJSON = entriesRowsJSON,
                           )

@app.route('/submit_review', methods=['POST'])
def submit_review():
    # Grabs all the potentially new form info
    if request.method == "POST":
        entry = {
            'entry_key' : None, 
            'tri_index' : request.form.get('interactionIndex', None),
            'tri_interaction_key' : request.form.get('intKey', None),
            "tri_incident_number": request.form.get('incNum', None),
            "tri_interaction_number": request.form.get('intNum', None),
            'user' : request.form.get('user', None),
            'reviewed' : 'YES',
            'video_of_force_incident' : request.form.get('VIDEO OF FORCE INCIDENT', None), 
            'good' : request.form.get('GOOD', None), 
            'bwc_command' : request.form.get('BWC COMMAND', None), 
            'bwc_user_at_time_of_incident' : request.form.get('BWC USER AT TIME OF INCIDENT', None), 
            'force_incident_serial_number' : request.form.get('fiSerial', None), 
            'force_incident_link' : request.form.get('fiLink', None), 
            'late_activation' : request.form.get('LATE ACTIVATION', None), 
            'early_deactivation' : request.form.get('EARLY DEACTIVATION', None), 
            'shared_with_ada' : request.form.get('SHARED WITH ADA', None), 
            'video_categorized_as_force_incident' : request.form.get('VIDEO CATEGORIZED AS FORCE INCIDENT', None), 
            'tri_number_entered_in_metadata' : request.form.get('TRI NUMBER ENTERED IN METADATA', None), 
            'multiple_videos_incident_by_user' : request.form.get('MULTIPLE VIDEOS OF INCIDENT BY USER', None), 
            'all_evidence_serial_numbers' : request.form.get('allSerial', None), 
            'all_evidence_links' : request.form.get('allLink', None),
            'dt_created' : request.form.get('dtCreated', None),
            'dt_committed' : None
            }
        
        formInput = list(entry.values())[3:]
        # The form input so it can check the info past the key
        if not (all((v == None or v == '') for v in formInput)) and entry['tri_interaction_key'] != '':
            submit_entry(entries, entry)

    return redirect(request.referrer)

# Manage page
@app.route('/manage')
def manage():
    entriesRowsJSON = json.dumps(entries.getAllRowsAsDict())

    return render_template(
                            'manage.html',
                            entriesRowsJSON = entriesRowsJSON,
                            )

# Import new data
@app.route('/import', methods=['POST'])
def importData():
    if request.method == "POST":
        # Gets the file input by the user
        file = request.files['file']
        if file.filename != '':
            # Calls function to import from excel
            manageDB.importFromFile(file, db)
    return redirect(request.referrer)

# Clear the data
@app.route('/clear', methods=['POST'])
def clear():
    if request.method == "POST":
        # See which tables are checked for deletion
        intCheck = request.form.get('interactionsCheck')
        entCheck = request.form.get('entriesCheck')

        # Deletes the tables based on what is checked
        if intCheck:
            interactions.delete()
        if entCheck:
            entries.delete()

    return redirect(request.referrer)

# Commit the data to the master database
@app.route('/commit')
def commit():
    # Time to store for the commit time
    now = datetime.now()
    nowStr = now.strftime("%m/%d/%Y %H:%M:%S")

    # Update the columns and add the commit
    db.execute(f"UPDATE entries SET dt_committed='{nowStr}'")

    # Copy tables to the master tables
    entries.copyTo(entriesMASTER)
    interactions.copyTo(interactionMASTER)
    return redirect(request.referrer)

# Export the tables to an excel sheet
@app.route('/export')
def export():
    # Connect to the tables and select all the row
    conn = db.connect()
    interactionsDF = pd.read_sql_query("SELECT * FROM interactions", conn)
    entriesDF = pd.read_sql_query("SELECT * FROM entries", conn)

    # Merge the tables and combine the entries with thei corresponding columns
    entriesInteractionsDF = entriesDF.merge(interactionsDF, on='tri_interaction_key', how='outer')
    # Sort the table by the index
    entriesInteractionsDF = entriesInteractionsDF.sort_values(by=['index'])
    # Drop the columns that are not needed on the excel sheet
    entriesInteractionsDF = entriesInteractionsDF.drop(['entry_key','tri_index','index','tri_interaction_key','tri_incident_number_x','tri_interaction_number_x', 'dt_created', 'dt_committed'],axis=1)

    # Save the output so the user can just download it
    output = io.BytesIO()
    with pd.ExcelWriter(output) as writer:
        entriesInteractionsDF.to_excel(writer, sheet_name='output', index=False)
    output.seek(0)

    response = make_response(output.read())
    response.headers['Content-Disposition'] = 'attachment; filename=recap-output.xlsx'
    response.mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    return response

# Delete a selected Entry or Interaction
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        # Get which ones are selected
        intToDelete = request.form.get('selectedInteraction')
        entryToDelete = request.form.get('selectedEntry')
        # Delete if any selection is made
        if intToDelete != "":
            interactions.delete(f'tri_interaction_key={intToDelete}')
        if entryToDelete != "":
            entries.delete(f'entry_key={entryToDelete}')

    return redirect(request.referrer)

# Execute an sqlite command
@app.route('/execute', methods=['POST'])
def execute():
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            # Runs a query on the sqlite using the function i made.
            db.executeQuery(command)
        except:
            pass

    return redirect(request.referrer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # FlaskUI(app=app, server="flask", width=800, height=600).run()