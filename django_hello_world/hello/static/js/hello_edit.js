function preSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').attr('disabled', 'disabled');
    $("#progress").attr('hidden', false);
    log('pre-submit');
}

function postSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').removeAttr('disabled');
    $("#progress").attr('hidden', true);
    setImageSize();
    log("posted");
}

$(document).ready(function () {

    var options = {
        target:'#image', // target element(s) to be updated with server response
        replaceTarget:true,
        beforeSubmit:preSubmitCallback, // pre-submit callback
        success:postSubmitCallback  // post-submit callback
        //timeout:   3000
    };

    $('#editForm').submit(
        function () {
            $(this).ajaxSubmit(options);
            log('submit');
            return false;
        }
    );
});