

function SetHorsesAndOdds(horsesAndOdds) {
    $("#horses").empty()
    horsesAndOdds.forEach(function (horse) {
        $("#horses").append(
            `<div id="HorseNamed${horse.Name}" class="row horse">
                <img height="50" class="horseImg" src="https://images2.minutemediacdn.com/image/upload/c_crop,h_1194,w_2121,x_0,y_34/f_auto,q_auto,w_1100/v1553786510/shape/mentalfloss/539787-istock-879570436.jpg"></img> <span>${horse.Name}</span>
            </div>`)
    });
}

$(function () {
    // Get that socketIo
    var socket = io();
    socket.on('connect', function () {
        socket.emit('Join room', $("#SessionId").text());
    });

    socket.on('Odds', function () {
        SetHorsesAndOdds
    })

    socket.on('HorsesChanged', function (data) {
        console.log("HorsesChanged triggered")
        console.log(data)
        SetHorsesAndOdds(data)
    })

    socket.on('Saldo', function (data) {
        console.log("")
        console.log(data)
        SetSaldo(data)
    })
})