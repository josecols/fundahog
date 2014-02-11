/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/

cancelarModal = false;

function capitalizarInicial(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function manejarRespuestaServidor(respuesta, reload) {
    respuesta = JSON.parse(respuesta);
    reload = typeof reload !== 'undefined' ? reload : true;

    switch (respuesta.flag) {
    case 0:
        $('#status').removeClass();
        $('#status').addClass('exito');
        $('#status').html('<i class="fa fa-check"></i>' + respuesta.msg);
        break;
    case -1:
        var html = '';
        $('#status').removeClass();
        $('#status').addClass('error');
        for (key in respuesta.errores) {
            html += '<i class="fa fa-exclamation"></i><b>' + capitalizarInicial(key) + ':</b> ' + respuesta.errores[key][0] + '<br>';
        }
        $('#status').html(html);
        break;
    }

    $('#status').slideToggle('fast');

    setTimeout(function () {
        $('#status').slideToggle('slow', function () {
            if (0 === respuesta.flag) {
                console.log(reload);
                if (reload)
                    location.reload();
            }
        });
    }, 3000);
}