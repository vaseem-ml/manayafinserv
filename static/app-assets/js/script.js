var flas_messages = '{{ get_flashed_messages() }}'
console.log('flas message', flas_messages)
var isRtl = $('html').attr('data-textdirection') === 'rtl';
setTimeout(function () {
toastr['error'](
    flas_messages,
    {
        closeButton: true,
        tapToDismiss: false,
        rtl: isRtl
    }
    );
}, 1000);