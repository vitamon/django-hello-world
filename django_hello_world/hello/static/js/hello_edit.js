function preSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').attr('disabled', 'disabled');
    $("#progress").attr('hidden', false);

    console.log(result.message);
    console.log(result.status);
}

function postSubmitCallback(result) {
    $("#editForm").find('input, textarea, button, select').removeAttr('disabled');
    $("#progress").attr('hidden', true);
    console.log('success');
    console.log(result.message);
    console.log(result.status);
}

function onErrorCallback(value) {
    console.log("error");
    postSubmitCallback({message:'ajax error',status:False})
}

$(document).ready(function () {

    var options = {
        beforeSubmit:preSubmitCallback,
        success:postSubmitCallback,
        error:onErrorCallback,
        dataType:'json',
        timeout:   3000
    };

    $('#editForm').submit(
        function () {
            $(this).ajaxSubmit(options);
            return false;
        }
    );
});