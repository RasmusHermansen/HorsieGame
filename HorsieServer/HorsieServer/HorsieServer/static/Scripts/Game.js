

function SetHorses(horses, socket) {
    $("#horses").empty()
    horses.forEach(function (horse) {
        $("#horses").append(
            `<li class="list-group-item">
            <img class="horse-icon" src="https://hotemoji.com/images/emoji/l/7tzudlpkm9sl.png">
            <div class="horse-details">
                <span>${horse.Name}</span>
                <br>
                <span class="odds" id="odds-${horse.id}">N/A</span>
            </div>
            <button id="btn-bet-large-${horse.id}" type="button" class="btn btn-secondary btn-bet pull-right">5</button>
            <button id="btn-bet-small-${horse.id}" type="button" class="btn btn-secondary btn-bet pull-right">1</button></li>`)
        $(`#btn-bet-large-${horse.id}`).click(function () {
            BetOnHorse(horse.id,5, socket)
        });
        $(`#btn-bet-small-${horse.id}`).click(function () {
            BetOnHorse(horse.id, 1, socket)
        });
    });
    Sortable.create(document.getElementById('horses'), {
        animation: 100,
        draggable: '.list-group-item',
        handle: '.list-group-item'
    });
}

function UpdateOdds(odds) {
    odds.forEach(function (oddAndHorse) {
        $(`#odds-${oddAndHorse.id}`).text(oddAndHorse.Odds)
    });
}

function SetSaldo(saldo) {
    $("#Standing").text(saldo);
}

function BetOnHorse(horse, amount, socket) {
    socket.emit('Bet', {
        'horse': horse,
        'amount': amount
    })
}

$(function () {
    // Get that socketIo
    var socket = io();
    socket.on('connect', function () {
        socket.emit('Join room');
    });

    socket.on('OddsChanged', function (odds) {
        UpdateOdds(odds)
    })

    socket.on('HorsesChanged', function (data) {
        // dirty and bad to pass socket :/
        SetHorses(data, socket)
    })

    socket.on('SaldoChanged', function (saldo) {
        SetSaldo(saldo)
    })
})