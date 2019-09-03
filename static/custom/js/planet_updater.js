//Static variables
var session_id_api_endpoint_url = '/session';
var planet_update_api_endpoint_url = '/planetInfo';

var session_id = get_session_id();
var celestialBody = '';

function get_ajax_headers(url, headers){
    console.log('Posting to: ' + url + headers);
    $.ajax({
            url: url,
            method: 'GET',
            headers: headers,
            success: function(data){
                celestialBody = JSON.parse(JSON.stringify(data));
            }
        })
}

function getSessionIdFromJSON(json){
    return JSON.parse(JSON.stringify(json)).session;
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
    console.log("Getting planet client update session: " + session_id);
    get_ajax_headers(planet_update_api_endpoint_url, {session: session_id});
    console.log(celestialBody);
    switch (celestialBody.name) {
        case "Sun":
            $('.carousel').carousel(0);
            break;
        case "Mercury":
            $('.carousel').carousel(1);
            break;
        case "Venus":
            $('.carousel').carousel(2);
            break;
        case "Earth":
            $('.carousel').carousel(3);
            break;
        case "Mars":
            $('.carousel').carousel(4);
            break;
        case "Pepe":
            $('.carousel').carousel(10);
            break;
    }
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
    $('.carousel').carousel({
        interval: false
    });
});