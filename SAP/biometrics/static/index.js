$(document).ready(function () {

    $("#btn_download_attendances").click(function (e) { 
        e.preventDefault();
        console.log('hehe')
        $.ajax({
            type: "GET",
            url: "/biometrics/download/attendance/",
            // data: {
            //     ip: "169.254.92.150",
            // },
            success: function (response) {
                console.log(response)
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                console.log(xhr, status, error);
            }
        });
    });
    $("#btn_download_employees").click(function (e) { 
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/biometrics/download/employees/",
            success: function (response) {
                console.log(response)
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                console.log(xhr, status, error);
            }
        });
        
    });

});
