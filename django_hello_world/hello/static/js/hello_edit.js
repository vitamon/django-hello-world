function preSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').attr('disabled', 'disabled');
    $("#progress").attr('hidden', false);
}

function postSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').removeAttr('disabled');
    $("#progress").attr('hidden', true);
}

function onErrorCallback() {

}

$(document).ready(function () {

    var options = {
        beforeSubmit:preSubmitCallback,
        success:postSubmitCallback,
        error:onErrorCallback
        //timeout:   3000
    };

    $('#editForm').submit(
        function () {
            $(this).ajaxSubmit(options);
            return false;
        }
    );
});