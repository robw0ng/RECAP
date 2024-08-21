const searchTerms = new Map();    
const searchTermsEntries = new Map();    

var eTable
$(document).ready(function () {
    eTable = $('#entryTable').DataTable({

        layout: {
            topStart: {
                search: {
                    placeholder: 'Search all columns...'
                }
            },
            topEnd: "info",
            bottomStart: "pageLength",
            bottomEnd: "paging",
            },
        order: [],
        serverSide: true,
        scrollY: 293.5,
        deferRender: true,
        scroller: true,
        stateSave: true,
        rowId: 'tri_interaction_key',
        ajax: {
            url: '/api/entries',
            data: function (d) {
                d.searchTerms = JSON.stringify(Object.fromEntries(searchTerms))
            }
        },
        columns: [
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function(data, type, row, meta) {
                    return '<button type="button" class="blue-btn">Select ></button>';
                }
            },
            {data: 'tri_index', sortable: false},
            {data: 'tri_interaction_key', visible: false, sortable: false},
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
            {data: 'entry_key', visible: true, sortable: false},
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
                    
                    if (column.footer().textContent != "Search:") {
                        column.footer().replaceChildren(input);

                        if (input.value != null && input.value != ""){
                            searchTermsEntries.set(input.placeholder, input.value)
                            table.ajax.reload(null, false);
                        }
                    }

                    input.addEventListener('keyup', () => {
                        console.log(input.value)
                        searchTermsEntries.set(input.placeholder, input.value)
                        localStorage.setItem(input.placeholder, input.value);
                        table.ajax.reload(null, false);
                    });
                });

            
        }
    });
    
    eTable.on('click', "tbody tr td:first-child button", (e) => {
        e.stopPropagation(); // Prevent event from bubbling up to parent elements
        let row = e.currentTarget.closest('tr');
        let classList = row.classList;
        
        if (classList.contains('selected')) {
            classList.remove('selected');
            selectedEntry = document.getElementById("selectedEntry")
            selectedEntry.value = null

        }
        else {
            eTable.rows('.selected').nodes().each((row) => row.classList.remove('selected'));
            classList.add('selected');    
            selectedEntry = document.getElementById("selectedEntry")
            selectedEntry.value = eTable.row(row).data()['entry_key'];
        }
    });
}
);


$(document).ready(function () {
    var table = $('#data').DataTable({

        layout: {
            topStart: {
                search: {
                    placeholder: 'Search all columns...'
                }
            },
            topEnd: "info",
            bottomStart: "pageLength",
            bottomEnd: "paging",
            },
        order: [],
        serverSide: true,
        scrollY: 293.5,
        deferRender: true,
        scroller: true,
        stateSave: true,
        ajax: {
            url: '/api/interactions',
            data: function (d) {
                d.searchTerms = JSON.stringify(Object.fromEntries(searchTerms))
            }
        },
        columns: [
            {
                data: null,
                orderable: false,
                searchable: false,
                render: function(data, type, row, meta) {
                    return '<button type="button" class="blue-btn">Select ></button>';
                }
            },
            {data: 'tri_interaction_key', visible: false, sortable: false},
            {data: 'index', sortable: false},
            {data: 'tri_incident_number', sortable: false},
            {data: 'tri_interaction_number', sortable: false},
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
                    
                    if (column.footer().textContent != "Search:") {
                        column.footer().replaceChildren(input);

                        if (input.value != null && input.value != ""){
                            searchTerms.set(input.placeholder, input.value)
                            table.ajax.reload(null, false);
                        }
                    }

                    input.addEventListener('keyup', () => {
                        console.log(input.value)
                        searchTerms.set(input.placeholder, input.value)
                        localStorage.setItem(input.placeholder, input.value);
                        table.ajax.reload(null, false);
                    });
                });

            
        }
    });
    
    table.on('click', "tbody tr td:first-child button", (e) => {
        e.stopPropagation(); // Prevent event from bubbling up to parent elements
        let row = e.currentTarget.closest('tr');
        let classList = row.classList;
        
        if (classList.contains('selected')) {
            classList.remove('selected');
            selectedInteraction = document.getElementById("selectedInteraction")
            selectedInteraction.value = null
            selectedEntry = document.getElementById("selectedEntry")
            selectedEntry.value = null;
            entryRow = document.getElementById(table.row(row).data()['tri_interaction_key'])
            entryRow.classList.remove('selected')
        }
        else {
            table.rows('.selected').nodes().each((row) => row.classList.remove('selected'));
            eTable.rows('.selected').nodes().each((row) => row.classList.remove('selected'));
            classList.add('selected');    
            selectedInteraction = document.getElementById("selectedInteraction")
            selectedInteraction.value = table.row(row).data()['tri_interaction_key'];
            selectedEntry = document.getElementById("selectedEntry")
            
            entryRow = document.getElementById(table.row(row).data()['tri_interaction_key'])
            entryRow.classList.add('selected')
            selectedEntry.value = entryRow.childNodes[20].innerHTML    
        }
    });
}
);