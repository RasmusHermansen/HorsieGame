$(function () {
    // Subscribe to btn click
    $("#GameInfoToggleBtn").click(function () {
        $(".gameContainer").toggle();
    }
})

/*
        var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function () {
            socket.emit('CreateSession');

            socket.on('message', function (data) {
                $("#SocketOutput").html = data
            })
        });
    })
*/