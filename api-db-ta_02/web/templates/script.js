$(document).ready(function() {
    // обработчик события на выбор маркета
    $('#market').change(function() {
        // отправляем AJAX-запрос на сервер с параметрами маркета и основной монеты
        $.ajax({
            url: '/get_available_pairs',
            type: 'POST',
            data: {
                'market': $('#market').val(),
                'base_currency': $('#base_currency').val(),
                'csrf_token': $('input[name=csrf_token]').val()
            },
            dataType: 'json',
            success: function(response) {
                // обновляем список доступных пар на странице
                updateCoinList(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    // обработчик события на выбор основной монеты
    $('#base_currency').change(function() {
        // отправляем AJAX-запрос на сервер с параметрами маркета и основной монеты
        $.ajax({
            url: '/get_available_pairs',
            type: 'POST',
            data: {
                'market': $('#market').val(),
                'base_currency': $('#base_currency').val(),
                'csrf_token': $('input[name=csrf_token]').val()
            },
            dataType: 'json',
            success: function(response) {
                // обновляем список доступных пар на странице
                updateCoinList(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

    // функция для обновления списка доступных пар на странице
    function updateCoinList(response) {
        var coinList = $('#coin_list');
        // очищаем список
        coinList.empty();
        // проходим по списку пар из ответа сервера и добавляем их в список на странице
        for (var i = 0; i < response.length; i++) {
            var coin = response[i];
            coinList.append('<li>' + coin + '</li>');
        }
    }
});
