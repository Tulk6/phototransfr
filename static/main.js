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
}
init_ws();
