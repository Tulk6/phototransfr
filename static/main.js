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
var current_image_caption = "";
var current_image_datetime = "";

var main_image_element = document.getElementById("main_image");
var image_caption_element = document.getElementById("image_caption");

function set_current_image(message) {
    var message_parts = message.split("|")
    current_image_index = message_parts[0];
    current_image_datetime = message_parts[1];
    current_image_caption = message_parts[2];
    main_image_element.src = get_file_from_image_index(current_image_index);
    image_caption_element.innerHTML = '<b>('+current_image_index+') '+current_image_datetime+':</b> '+current_image_caption;
}

function emit_next(){
    ws.send("next");
}

function emit_prev(){
    ws.send("prev");
}
 
function emit_index(evt){
    evt.preventDefault()
    var message = document.getElementById('emit_index').value;
    ws.send(message);
    return false;
}
var emit_index_form = document.getElementById('emit_index_form');
emit_index_form.addEventListener('submit', emit_index);

window.onkeydown = function(event) {
    if (event.keyCode == 37) {
        emit_prev();
    }else if (event.keyCode = 39) {
        emit_next();
    }
};


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
        set_current_image(evt.data);
    }
}
init_ws();

