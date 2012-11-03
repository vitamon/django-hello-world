function preSubmitCallback() {
    $("#editForm").find('input, textarea, button, select').attr('disabled', 'disabled');
    $("select, input[type='file']").attr('disabled', true);
    $.uniform.update();
    $("#progress").attr('hidden', false);
    $(".alert").hide();
    return true
}

function postSubmitCallback(data) {
    if (data.status == true) {
        $(".alert").addClass("alert-success").removeClass("alert-error");
    } else {
        $(".alert").addClass("alert-error").removeClass("alert-success");
    }
    $(".alert #message").html(data.message);
    $(".alert").show();

    $("#editForm").find('input, textarea, button, select').removeAttr('disabled');
    $("#progress").attr('hidden', true);
    $("select, input[type='file']").attr('disabled', false);
    $.uniform.update();
}

function onErrorCallback(data) {
    postSubmitCallback({status:false, message:"error"})
}

function previewImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#photo').attr('src', e.target.result)
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function () {
    $(".close").on('click', function () {
        $(".alert").hide();
    });

    $(":file").uniform();

    $("#id_photo")[0].onchange = function () {
        previewImage(this);
    };

    var options = {
        beforeSubmit:preSubmitCallback,
        success:postSubmitCallback,
        error:onErrorCallback,
        dataType:'json',
        timeout:3000
    };

    $('#editForm').submit(
        function () {
            $(this).ajaxSubmit(options);
            return false;
        }
    );
});