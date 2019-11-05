

function SetHorses(horses, socket) {
    $("#horses").empty()
    horses.forEach(function (horse) {
        $("#horses").append(
            `<li class="list-group-item" id="li-${horse.id}">
            <img class="horse-icon" src="static/Icons/${horse.icon}">
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

function SetPlayers(players, socket) {
    $("#people").empty()
    players.forEach(function (player) {
        $("#people").append(
            `<li class="list-group-item-drink" id="li-${player.id}">
            <span class="Player-Alias">${player.Alias}</span>
            <button id="btn-drink-large-${player.id}" type="button" class="btn btn-secondary btn-drink pull-right">5 Beer</button>
            <button id="btn-drink-medium-${player.id}" type="button" class="btn btn-secondary btn-drink pull-right">3 Shot</button>
            <button id="btn-drink-small-${player.id}" type="button" class="btn btn-secondary btn-drink pull-right">1 Sip</button></li>`)
        $(`#btn-drink-large-${player.id}`).click(function () {
            GiveDrink(player.id, 5, socket)
        });
        $(`#btn-drink-medium-${player.id}`).click(function () {
            GiveDrink(player.id, 3, socket)
        });
        $(`#btn-drink-small-${player.id}`).click(function () {
            GiveDrink(player.id, 1, socket)
        });
    });
    Sortable.create(document.getElementById('people'), {
        animation: 100,
        draggable: '.list-group-item-drink',
        handle: '.list-group-item-drink'
    });
}

function UpdateOdds(odds) {
    odds.forEach(function (oddAndHorse) {
        $(`#odds-${oddAndHorse.id}`).text(Math.round(oddAndHorse.Odds*100)/100)
    });
}

function SetSaldo(saldo) {
    $("#Standing").text(saldo);
}

function GiveDrink(player, drink, socket) {
    socket.emit('GiveDrink', {
        'player': player,
        'drink':drink
    })
}

function BetOnHorse(horse, amount, socket) {
    socket.emit('Bet', {
        'horse': horse,
        'amount': amount
    })
}

function FormatTopThree(topThree) {
    $(".FirstPlace").removeClass("FirstPlace")
    $(`#li-${topThree[0]}`).addClass("FirstPlace")
    if (topThree.length > 1) {
        $(".SecondPlace").removeClass("SecondPlace")
        $(`#li-${topThree[1]}`).addClass("SecondPlace")
    }
    if (topThree.length > 2) {
        $(".ThirdPlace").removeClass("ThirdPlace")
        $(`#li-${topThree[2]}`).addClass("ThirdPlace")
    }
}

$(function () {
    $("#ShowPeople").click(function () {
        $("#horses").hide();
        $("#people").show();
    });
    $("#ShowHorses").click(function () {
        $("#people").hide();
        $("#horses").show();
    });
})

$(function () {
    // Get that socketIo
    var socket = io();
    socket.on('connect', function () {
        socket.emit('Join room');
    });

    socket.on('disconnect', function () {
        // TODO: Notify of disconnect
    })

    socket.on('OddsChanged', function (odds) {
        UpdateOdds(odds)
    })

    socket.on('HorsesChanged', function (data) {
        SetHorses(data, socket) // Slightly sketchy to pass socket?
    })

    socket.on('PlayersChanged', function (data) {
        SetPlayers(data, socket) // Slightly sketchy to pass socket?
    })

    socket.on('SaldoChanged', function (saldo) {
        SetSaldo(saldo)
    })

    socket.on('RaceOver', function (topThree) {
        socket.emit('GetSaldo')
        $(".btn-bet").prop("disabled", false);
        FormatTopThree(topThree)
    })

    socket.on('BettingDisabled', function () {
        $(".btn-bet").prop("disabled", true);
        // TODO: Add some visual stating that betting is disabled for now
    })

    socket.on('message', function (msg) {
        var dateStamp = new Date().toTimeString().replace(/.*(\d{2}:\d{2}:\d{2}).*/, "$1");
        $("#SocketMessage").text(dateStamp + " " + msg) 
        // TODO: Add this to the styling
    })

    // TODO: Allow for one user to send a 'drink' to another player :) :) :) :)
    // 5$ => 1 whole drink?, 1$ => 1 zip?, 3$ => Small shot?
})