function check(value, options){
    if (value == null){
        return
    }

    for(i=0; i<options.length; i++){
        options[i].checked = false;
    }
    switch(value){
        case 'YES':
            options[0].checked = true;
            return;

        case 'NO':
            options[1].checked = true;
            return;
        
        case 'NO VIDEO':
            options[2].checked = true;
            return;

        default:
            return;
    }
}

function clear(options){
    for(i=0; i<options.length; i++){
        options[i].checked = false;
    }
}

function fillForm(entry){
    console.log("filling form with")
    console.log(entry)

    vofi = document.getElementsByName("VIDEO OF FORCE INCIDENT");
    good = document.getElementsByName("GOOD");
    bwcCom = document.getElementsByName("BWC COMMAND");
    bwcUser = document.getElementsByName("BWC USER AT TIME OF INCIDENT");

    fiSerial = document.getElementById("fiSerial");
    fiSerial.value = entry["force_incident_serial_number"];


    fiLink = document.getElementById("fiLink");
    fiLink.value = entry["force_incident_link"];

    late = document.getElementsByName("LATE ACTIVATION");
    early = document.getElementsByName("EARLY DEACTIVATION");
    shared = document.getElementsByName("SHARED WITH ADA");
    categorized = document.getElementsByName("VIDEO CATEGORIZED AS FORCE INCIDENT");
    triEntered = document.getElementsByName("TRI NUMBER ENTERED IN METADATA");
    multiple = document.getElementsByName("MULTIPLE VIDEOS OF INCIDENT BY USER");

    allSerial = document.getElementById("allSerial");
    allSerial.value = entry["all_evidence_serial_numbers"];

    allLink = document.getElementById("allLink");
    allLink.value = entry["all_evidence_links"];
    
    entryUID = document.getElementById("entryUID");
    entryUID.value = entry["entry_key"];

    user = document.getElementById("user");
    user.value = entry["user"];

    dt = document.getElementById("dtCreated");
    dt.value = entry["dt_created"];

    triIndex = document.getElementById("interactionIndex");
    triIndex.value = entry["tri_index"];

    check(entry["video_of_force_incident"], vofi);
    check(entry["good"], good);
    check(entry['bwc_command'], bwcCom);
    check(entry['bwc_user_at_time_of_incident'], bwcUser)
    check(entry['late_activation'], late);
    check(entry['early_deactivation'], early);
    check(entry['shared_with_ada'], shared);
    check(entry['video_categorized_as_force_incident'], categorized);
    check(entry['tri_number_entered_in_metadata'], triEntered);
    check(entry['multiple_videos_incident_by_user'], multiple)        
    return
}

function clearForm(){
    vofi = document.getElementsByName("VIDEO OF FORCE INCIDENT");
    good = document.getElementsByName("GOOD");
    bwcCom = document.getElementsByName("BWC COMMAND");
    bwcUser = document.getElementsByName("BWC USER AT TIME OF INCIDENT");

    fiSerial = document.getElementById("fiSerial");
    fiSerial.value = null;
    fiLink = document.getElementById("fiLink");
    fiLink.value = null;

    late = document.getElementsByName("LATE ACTIVATION");
    early = document.getElementsByName("EARLY DEACTIVATION");
    shared = document.getElementsByName("SHARED WITH ADA");
    categorized = document.getElementsByName("VIDEO CATEGORIZED AS FORCE INCIDENT");
    triEntered = document.getElementsByName("TRI NUMBER ENTERED IN METADATA");
    multiple = document.getElementsByName("MULTIPLE VIDEOS OF INCIDENT BY USER");

    allSerial = document.getElementById("allSerial");
    allSerial.value = null;
    allLink = document.getElementById("allLink");
    allLink.value = null;

    entryUID = document.getElementById("entryUID");
    entryUID.value = null;

    user = document.getElementById("user");
    user.value = null;

    dt = document.getElementById("dtCreated");
    dt.value = null;

    triIndex = document.getElementById("interactionIndex");
    triIndex.value = null;

    clear(vofi);
    clear(good);
    clear(bwcCom);
    clear(bwcUser);
    clear(late);
    clear(early);
    clear(shared);
    clear(categorized);
    clear(triEntered);
    clear(multiple);
    return
}

const searchTerms = new Map();
var view = new Map() 

$(document).ready(function () {
    var table = $('#data').DataTable({

        layout: {
            topEnd: {},
            topStart: {
                div: {
                    className: 'rangeDiv',
                    id: 'rangeDiv',
                    html: `
                    <div class="row">
                        <div class="line col">
                            <div class="line col" style="padding-top:2px;">
                                <label class="table-text" id="showRangeText">Show Range:</label>
                            </div>
                            <div class="line col">
                                <input type="text" class="range-input filter-input form-control border rounded" id="startRange" placeholder="Start">
                            <div class="line col" style="padding-top:2px;">
                                <label class="table-text" id="toText">to</label>
                            </div>
                            <div class="line col">
                                <input type="text" class="range-input filter-input form-control border rounded" id="endRange" placeholder="End">
                            </div>
                        </div>
                    </div>
                    `
                },
                search: {
                    placeholder: 'Search all columns...'
                }
            },
            bottomStart: "pageLength",
            bottomEnd: "info",
        },
        order: [],
        serverSide: true,
        scrollY: 750,
        deferRender: true,
        scroller: true,
        stateSave: true,
        ajax: {
            url: '/api/entries_interactions',
            data: function (d) {
               d.searchTerms = JSON.stringify(Object.fromEntries(searchTerms)),
               d.view = JSON.stringify(Object.fromEntries(view))
            }
        },
        columns: [
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function(data, type, row, meta) {
                    return '<button type="button" class="purple-btn">Select ></button>';
                }
            },
            {data: 'tri_interaction_key', visible: false, sortable: false},
            {data: 'tri_index', sortable: false},
            {data: 'tri_incident_number', sortable: false},
            {data: 'tri_interaction_number', sortable: false},

            {data: 'reviewed', sortable: false},
            {data: 'video_of_force_incident', sortable: false},
            {data: 'good', sortable: false},
            {data: 'bwc_command', sortable: false},
            {data: 'bwc_user_at_time_of_incident', sortable: false},
            {data: 'force_incident_serial_number', sortable: false},
            {data: 'force_incident_link', sortable: false},
            {data: 'late_activation', sortable: false},
            {data: 'early_deactivation', sortable: false},
            {data: 'shared_with_ada', sortable: false},
            {data: 'video_categorized_as_force_incident', sortable: false},
            {data: 'tri_number_entered_in_metadata', sortable: false},
            {data: 'multiple_videos_incident_by_user', sortable: false},
            {data: 'all_evidence_serial_numbers', sortable: false},
            {data: 'all_evidence_links', sortable: false},
            {data: 'user', sortable: false},

            {data: 'mos_command_description', sortable: false},
            {data: 'mos_rank_code', sortable: false},
            {data: 'mos_full_name', sortable: false},
            {data: 'mos_tax_number', sortable: false},
            {data: 'occurrence_date', sortable: false},
            {data: 'occurrence_time', sortable: false},
            {data: 'tri_level', sortable: false},
            {data: 'encounter_type_description', sortable: false}
        ],

        initComplete: function () {
            this.api()
                .columns()
                .every(function () {
                    let column = this;
                    let title = column.footer().textContent;

                    let input = document.createElement('input');
                    input.placeholder = title;
                    input.id = title
                    input.className='form-control'
                    input.value = localStorage.getItem(input.placeholder)
                    
                    if (column.footer().textContent != "Search:" && column.footer().textContent != "TRI Index") {
                        column.footer().replaceChildren(input);

                        if (input.value != null && input.value != ""){
                            searchTerms.set(input.placeholder, input.value)
                            table.ajax.reload();
                        }
                    }

                    input.addEventListener('keyup', () => {
                        console.log(input.value)
                        searchTerms.set(input.placeholder, input.value)
                        localStorage.setItem(input.placeholder, input.value);
                        table.ajax.reload();
                    });
                });

                startIndexElement = document.getElementById("startRange");
                startIndexElement.value = localStorage.getItem("Start")
                if (startIndexElement.value != null && startIndexElement.value != ""){
                    view.set("Start", startIndexElement.value)
                    table.ajax.reload();
                }

                startIndexElement.addEventListener('keyup', () => {
                    console.log(startIndexElement.value)
                    view.set("Start", startIndexElement.value)
                    localStorage.setItem("Start", startIndexElement.value);
                    table.ajax.reload();
                });

                endIndexElement = document.getElementById("endRange");
                endIndexElement.value = localStorage.getItem("End")
                if (endIndexElement.value != null && endIndexElement.value != ""){
                    view.set("End", endIndexElement.value)
                    table.ajax.reload();
                }

                endIndexElement.addEventListener('keyup', () => {
                    console.log(endIndexElement.value)
                    view.set("End", endIndexElement.value)
                    localStorage.setItem("End", endIndexElement.value);
                    table.ajax.reload();
                });
        }
    });
    
    table.on('click', "tbody tr td:first-child button", (e) => {
        e.stopPropagation(); // Prevent event from bubbling up to parent elements
        let row = e.currentTarget.closest('tr');
        let classList = row.classList;

        if (classList.contains('selected')) {
            classList.remove('selected');

            intKeyElement = document.getElementById("intKey");
            intKeyElement.value = null

            incNumElement = document.getElementById("incNum");
            incNumElement.value = null

            intNumElement = document.getElementById("intNum");
            intNumElement.value = null

            clearForm();
        }
        else {
            table.rows('.selected').nodes().each((row) => row.classList.remove('selected'));
            classList.add('selected');

            intKeyElement = document.getElementById("intKey");
            intKeyElement.value = table.row(row).data()['tri_interaction_key']

            for(var i=0; i<entries.length; i++){
                entry = entries[i]

                var entryTriKey = entry["tri_interaction_key"];
                if ( entryTriKey == table.row(row).data()['tri_interaction_key']){
                    fillForm(entry)
                    break;
                }
                else if (entryTriKey != table.row(row).data()['tri_interaction_key']){
                    clearForm()
                }
            }

            incNumElement = document.getElementById("incNum");
            incNumElement.value = table.row(row).data()['tri_incident_number'];

            intNumElement = document.getElementById("intNum");
            intNumElement.value = table.row(row).data()['tri_interaction_number'];
        }
    });
}
);