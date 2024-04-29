$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/biometrics/attendances/fetch/",
        success: function (response) {
            console.log(response)
        }
    });
    const employees_table = new DataTable("#table_records", {
        autoTableLayout: true,
        ordering: false,
        // autoWidth: true,
        ajax: {
            type: "GET",
            url: "/biometrics/attendances/fetch/",
            dataSrc: 'records',
        },
        language: {
            error: function(errors, settings, techNote, table) {
                // Display the error message
                console.log(errors);
            }
        },
        columns: [{
                data: 'id'
            },
            {
                data: 'uid'
            },
            {
                data: 'employee__dv_name'
            },
            {
                render:function(data, type, row) {
                    let timestamp = row.timestamp;
                    let date = new Date(timestamp);
                    let formattedDate = date.toLocaleString()
                    return formattedDate
                }
            },
            {
                data: 'status'
            },
            {
                data: 'punch'
            },  
            {
                data: 'employee_id'
            },
        ],

        createdRow: function(row, data, index) {
            $(row).attr('data-id', data.id);

        },
    });
});