/* window.onload(function(){
    var socket = io();
    socket.on('myresponse', function(msg) {
        console.log('<p>Received: ' + msg.data + '</p>');
    });
});

function emitmymessage(){
    socket.emit('myevent', {data: "what up?"});
}
*/

function get_file_from_image_index(index) {
    return "static/photos/"+index+".jpg";
}

var current_image_index = 0;

var main_image_element = document.getElementById("main_image");

function set_current_image_index(index) {
    current_image_index = index;
    main_image_element.src = get_file_from_image_index(index);
}

function emit_next(){
    ws.send("next");
}

function emit_prev(){
    ws.send("prev");
}
 

function openFullscreen(){
    var elem = document.getElementById("main_image");
    //elem.webkitRequestFullscreen();
    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { // Safari
        elem.webkitRequestFullscreen();
    }
}

var ws = null;
function init_ws(){
    ws = new WebSocket("{{ url_for('websocket', _external=True, _scheme='ws') }}");

    ws.onmessage = function(evt) {
        console.log(evt.data);
        set_current_image_index(evt.data);
    }
}
init_ws();

