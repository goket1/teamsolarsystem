//Static variables
var session_id_api_endpoint_url = '/session';
var planet_update_api_endpoint_url = '/client_update?scanner_id=';

var session_id = get_session_id();

function getSessionIdFromJSON(json){
    return JSON.parse(JSON.stringify(json)).session
}

function get_session_id(){
    console.log("Gettting session from: " + session_id_api_endpoint_url);
    $.get(session_id_api_endpoint_url,
     function(data){
        session_id = getSessionIdFromJSON(data);
        console.log("Got session: " + session_id);
    })
}

function update_planet() {
    console.log("Getting planet client update");
    $.get(planet_update_api_endpoint_url + session_id,
    function(data) {
        console.log("planet client update response:" + data);
        if (data == "('Mars',)") {
            $('.carousel').carousel(4);
        } else if (data == "('Earth',)") {
            $('.carousel').carousel(3);
        }
    })
}

//Runs on page load
$( document ).ready(function() {
    var t1 = setInterval(update_planet, 100);
    var t2 = setInterval(get_session_id, 250);

    if(!session_id){
        $('#sessionIDModal').modal('show')
    }else{
        document.getElementById("set_session_id").innerHTML = session_id;
    }
});