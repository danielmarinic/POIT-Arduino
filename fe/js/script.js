$(document).ready(function () {
    let socket;
    let led_color = 'red';
    let id = 1;

    let table = $('#dataTable').DataTable({"order": [[0, "desc"]]});

    $('#start-button').click(function () {
        if ($(this).text() === 'Stop') {
            $(this).text('Start');
            socket.on('disconnect', function (msg) {
                console.log(msg);
            });
            socket.off();
        } else {
            socket = io.connect('ws://localhost:5000');
            socket.on('connect', function (msg) {
                console.log(msg);
            });
            socket.on('serial_message', function (msg) {
                // console.log(msg);
                addRowToTable(msg, id, table);
                id++;
            });
            $(this).text('Stop');
        }
    });

    $('#led').click(function () {
        if ($(this).text() === 'OFF') {
            $(this).text('ON');
            $('#led-icon').removeClass('text-gray-300').addClass('text-warning');
            changeLedStatus(true, led_color);
        } else {
            $(this).text('OFF');
            $('#led-icon').removeClass('text-warning').addClass('text-gray-300');
            changeLedStatus(false, led_color);
        }
    });

    $('.led-color').click(function () {
        let color = $(this).prop("value");
        $(this).children('i').removeClass('fa-circle').addClass('fa-circle-notch');
        $('.led-color[value="led-'+led_color+'"]').children('i').removeClass('fa-circle-notch').addClass('fa-circle');
        led_color = color.replace('led-', '');
    })
});

function changeLedStatus(status, led_color) {
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/led",
        data: JSON.stringify({sensor: 'led', led_enabled: status, led_color: led_color.replace('led-', '') }),
        success: function () {
            console.log("ok");
        },
        error: function () {
            console.log("fail");
        },
        contentType : 'application/json',
        dataType: 'html'
    });
}

function addRowToTable(msg, id, table) {
    let data = JSON.parse(msg.message);
    let row = [];
    row.push(id);
    row.push(data.temperature + ' °C');
    row.push(data.humidity + '%');
    row.push(new Date().toTimeString());
    table.row.add(row).draw(false);
}
