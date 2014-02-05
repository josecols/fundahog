/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Carga de imágenes con modal
*/
function pseudoUUID() {
    return 'xxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

$(document).ready(function () {
    if (jQuery.browser.mobile) {
        $('.pop.fancybox').hide();
    }

    $('input[name=imagen]').change(function () {
        var titulo;
        var album = $(this).attr('data-album').match(/[0-9]+/);
        if ('' === (titulo = $('#titulo-' + $(this).attr('data-album')).val()))
            titulo = pseudoUUID();

        $(this).upload(urlAgregarImagen, {
            'titulo': titulo,
            'album': album,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            manejarRespuestaServidor(JSON.stringify(json));
        });
    });
});