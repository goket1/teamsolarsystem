// Password match

$passwords_match_message = "Passwords match";
$passwords_dont_match_message = "Passwords don't match!";

$passwords_match_color = "green"
$passwords_dont_match_color = "red"

$('#registrationPassword, #registrationPasswordRepeat, #registrationUserName').on('keyup', function () {
    if ($('#registrationPassword').val() != '') {
        if ($('#registrationPassword').val() == $('#registrationPasswordRepeat').val()) {
            $('#password_message').html($passwords_match_message).css('color', $passwords_match_color);
            if ($('#registrationUserName').val() != '') {
                $("#registrationSubmitButton").prop("disabled", false);
            }
            else{
                $("#registrationSubmitButton").prop("disabled", true);
            }
        } else {
            $('#password_message').html($passwords_dont_match_message).css('color', $passwords_dont_match_color);
            $("#registrationSubmitButton").prop("disabled", true);
        }
    } else {
        $('#password_message').html('Empty').css('color', $passwords_dont_match_color);
        $("#registrationSubmitButton").prop("disabled", true);
    }
});

/* attach a submit handler to the form */
$("#registerForm").submit(function (event) {

    /* stop form from submitting normally */
    event.preventDefault();

    /* get the action attribute from the <form action=""> element */
    var $form = $(this),
        url = $form.attr('action');

    var posting = $.post(url, {
        registrationUserName: $('#registrationUserName').val(),
        registrationPassword: $('#registrationPassword').val()
    });

    posting.done(function (data) {
        if (data == 0) {
            $('#user_name_message').html('User name taken').css('color', 'red');
        } else {
            $('#registerModal').modal('toggle');
        }
    });
});