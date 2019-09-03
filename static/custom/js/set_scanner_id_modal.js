function post_ajax_headers(url, headers){
    console.log('Posting to: ' + url + headers);
    $.ajax({
            url: url,
            method: 'POST',
            headers: headers,
            success: function(data){
                return data;
            }
        })
}

//Set scanner id input field changed
$(document).ready(function(){
    $("#set_session_id_modal").on('change paste keyup input',function(e){
        var session_input_field = $('#set_session_id_modal').val();
        if(session_input_field.length === 6){
            post_ajax_headers('/session', {session: session_input_field});
            $('#sessionIDModal').modal('hide');
            $("#set_session_id").val(session_input_field);
        }
    });
});