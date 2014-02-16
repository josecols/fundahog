/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar imágenes de los álbumes.
 * @class Galeria
 */

/**
 * Genera un código pseudo uuid de 8 dígitos aleatorios.
 *
 * @method pseudoUUID
 * @return {String} Cadena de texto con código pseudo uuid.
 **/
function pseudoUUID() {
    return 'xxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

$(document).ready(function () {
    $('input[name=imagen]').change(function () {
        guardar(this);
    });

    /**
     * Realiza la consulta al servidor para agregar una nueva Imagen.
     *
     * @method guardar
     * @param input {Object} Input que dispara el evento y que contiene el ID del álbum donde se agregará la imagen.
     * @param urlAgregarImagen {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar(input) {
        var titulo;
        var album = $(input).attr('data-album');
        var albumPK = album.match(/[0-9]+/);
        if ('' === (titulo = $('#titulo-' + $(input).attr('data-album')).val()))
            titulo = pseudoUUID();

        $('#progress-' + album).show();
        $.fancybox.update();

        $(input).upload(urlAgregarImagen, {
            'titulo': titulo,
            'album': albumPK,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            Admin.manejarRespuestaServidor(JSON.stringify(json));
        }, function (progress, value) {
            $('#progress-' + album + ' > span').width(value + '%');
        });
    }

    /**
     * Realiza la consulta al servidor para borrar una Imagen existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID de la Imagen a borrar.
     * @param urlBorrarImagen {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
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
                Admin.manejarRespuestaServidor(json);
            });
        }
    }

    $('.thumbnail .borrar').click(function () {
        borrar(this);
        cancelarModal = true;
    });
});