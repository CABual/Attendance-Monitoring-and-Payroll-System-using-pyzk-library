    $(document).ready(function () {
 
    const employees_table = new DataTable("#table_records", {
        autoTableLayout: true,
        // autoWidth: true,
        ajax: {
            type: "GET",
            url: "/biometrics/employees/fetch/",
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
                data: 'dv_name'
            },
            {
                data: 'dv_user_id'
            },
        ],

        createdRow: function(row, data, index) {
            $(row).attr('data-id', data.id);

        },
    });
}); 