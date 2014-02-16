/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo se encarga de gestionar la comunicación con el servidor que es originada en otros módulos.
 * @class Admin
 */
Admin = {};

/**
 * Se encarga de controlar la aparición de modales en la página. Si es verdadera, ningún modal será mostrado.
 * Los modales son las ventanas internas en la página, creadas con la librería fancybox.js.
 *
 * @property cancelarModal
 * @static
 * @type Boolean
 * @default false
 */
cancelarModal = false;

/**
 * Retorna el string con la primera letra en mayúscula.
 *
 * @method capitalizarInicial
 * @param string {String} Cadena de texto con inicial no capitalizada.
 * @return {String} Cadena de texto con inicial capitalizada.
 **/
Admin.capitalizarInicial = function (string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * Muestra la respuesta del servidor al cliente de forma amigable utilizando el elemento HTML #status.
 *
 * @method manejarRespuestaServidor
 * @param respuesta {JSON} JSON de comunicación según estándar definido.
 * @param reload {Boolean} Indica si la página debe ser recargada después de mostrar el mensaje. Es true por defecto.
 **/
Admin.manejarRespuestaServidor = function (respuesta, reload) {
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
            html += '<i class="fa fa-exclamation"></i><b>' + Admin.capitalizarInicial(key) + ':</b> ' + respuesta.errores[key][0] + '<br>';
        }
        $('#status').html(html);
        break;
    }

    $('#status').slideToggle('fast');

    setTimeout(function () {
        $('#status').slideToggle('slow', function () {
            if (0 === respuesta.flag) {
                if (reload)
                    location.reload();
            }
        });
    }, 3000);
}