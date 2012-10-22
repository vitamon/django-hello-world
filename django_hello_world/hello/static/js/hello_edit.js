function preSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').attr('disabled', 'disabled');
    $("#progress").attr('hidden', false);
}

function postSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').removeAttr('disabled');
    $("#progress").attr('hidden', true);
}

$(document).ready(function () {

    var options = {
        target:'#image', // target element(s) to be updated with server response
        replaceTarget:true,
        beforeSubmit:preSubmitCallback,
        success:postSubmitCallback
        //timeout:   3000
    };

    $('#editForm').submit(
        function () {
            $(this).ajaxSubmit(options);
            return false;
        }
    );
});