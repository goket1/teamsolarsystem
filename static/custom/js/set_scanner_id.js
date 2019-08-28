    <script>
    // Wait for the dom to be loaded
    document.addEventListener('DOMContentLoaded', function(event) {

        // Setup an XMLHttpRequest / AJAX request
        var request = new XMLHttpRequest();
        request.open('GET', '/sessions');

        // Setup an "event listener".
        request.onload = function() {
            if (request.status >= 200 && request.status < 400){
                var response = JSON.parse(request.responseText.toString());
                console.log(response.sessions);
                response.sessions.forEach(function(el){
                    addListEntry(el, "session id");
                });
            }
        };

        // Send our request
        request.send();
    });


    // Break the list adding code into a function for easier re-use
    function addListEntry(value, text) {

        // Create a new option element.
        var optionNode =  document.createElement("option");

        // Set the value
        optionNode.value = value;

        // create a text node and append it to the option element
        optionNode.appendChild(document.createTextNode(text));

        // Add the optionNode to the datalist
        document.getElementById("hosting-plan").appendChild(optionNode);

    }
    </script>