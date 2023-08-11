

(function (window, undefined) {
    "use strict";
    /*
    NOTE:
    ------
    PLACE HERE YOUR OWN JAVASCRIPT CODE IF NEEDED
    WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR JAVASCRIPT CODE PLEASE CONSIDER WRITING YOUR SCRIPT HERE.  */
    if ($("#activeSideBar").length) {
        $("#" + $("#activeSideBar").val()).addClass("active");
    }
    if ($("#siteToast").length) {
        // On load Toast
        setTimeout(function () {
            toastr[$("#siteToast").attr("data-type")](
                $("#siteToast").attr("data-title"),
                $("#siteToast").attr("data-info"),
                {
                    closeButton: true,
                    tapToDismiss: false,
                    rtl: $("html").attr("data-textdirection") === "rtl",
                }
            );
        }, 200);
    }
    //loader on submit
    $("form").submit(function (e) {
        if ($(this).valid()) {
            // blockUI();
        } else {
            e.preventDefault();
        }
    });

    if ($(".confirm-delete").length) {
        $(".confirm-delete").click(() => {
            return confirm("Are you sure ?");
        });
    }
    $(document).ajaxStart(function (e) {
        // blockUI();
    });
    $(document).ajaxStop(function (e) {
        // setTimeout($.unblockUI, 100);
    });
    $(window).on("load", function () {
        if (feather) {
            feather.replace({
                width: 14,
                height: 14,
            }); 
        }
        if ($(".date-picker").length) {
            $(".date-picker").flatpickr();
        }
    });
})(window);



//updating employee data
function update_employee(employee_data) {
    $('#update-first-name').val(employee_data.first_name)
    $('#update-last-name').val(employee_data.last_name)
    $('#update-email').val(employee_data.email)
    $('#update-mobile').val(employee_data.mobile)
    $('#update-birthdate').val(employee_data.dob)
    $('#update-designation').val(employee_data.designation)
    $('#update-gender').val(employee_data.gender)
    $('#update-status').val(employee_data.status)

    $('#update-employee-id').val(employee_data._id)

}

function update_bank(bank_data) {
    $('#update-name').val(bank_data.name)
    
    $('#update-status').val(bank_data.status)

    $('#update-bank-id').val(bank_data._id)

}

function update_client_card(client_card_data) {
    console.log('this is client data', client_card_data)
    $('input[type="checkbox"]').prop('checked', false);
    
    for (var i=0; i<client_card_data['employees'].length; i++) {
        console.log('this is id ',client_card_data['employees'][i]['_id'])
        $('#'+client_card_data['employees'][i]['_id']+"_").prop('checked', true);
    }

    $('#edit_card_status').val(client_card_data.status);
    $('#edit_card_id').val(client_card_data._id)
    


}