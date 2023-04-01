

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