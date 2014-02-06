/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Carga de imágenes con modal para galería
*/

function pseudoUUID() {
    return 'xxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

$(document).ready(function () {
    $('input[name=imagen]').change(function () {
        var titulo;
        var album = $(this).attr('data-album');
        var albumPK = album.match(/[0-9]+/);
        if ('' === (titulo = $('#titulo-' + $(this).attr('data-album')).val()))
            titulo = pseudoUUID();

        $('#progress-' + album).show();
        $.fancybox.update();

        $(this).upload(urlAgregarImagen, {
            'titulo': titulo,
            'album': albumPK,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            manejarRespuestaServidor(JSON.stringify(json));
        }, function (progress, value) {
            $('#progress-' + album + ' > span').width(value + '%');
        });
    });

    function borrar(boton) {
        var pk = $(boton).attr('data-imagen');
        var respuesta = confirm("¿Está seguro que deasea eliminar la imagen?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarImagen,
                data: 'imagen=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                manejarRespuestaServidor(json);
            });
        }
    }

    $('.thumbnail .borrar').click(function () {
        borrar(this);
        cancelarModal = true;
    });
});