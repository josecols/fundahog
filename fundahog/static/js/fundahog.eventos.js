/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar Eventos.
 * @class Eventos
 */

/**
 * Editor enriquecido existente en la página.
 *
 * @property ckeditor
 * @static
 * @type Object
 * @default null
 */
ckeditor = null;

/**
 * Indica si el editor está funcionando en modo inline
 *
 * @property inline
 * @static
 * @type Boolean
 * @default false
 */
inline = false;

$(document).ready(function () {
    ckeditor = CKEDITOR.replace('evento_contenido');

    $('#nuevo').click(function () {
        $('.formulario.admin').slideToggle('fast');
        $("html, body").animate({
            scrollTop: 0
        }, "slow");
        $('#guardar').toggle();
    });

    $('.borrar').click(function () {
        borrar(this);
    });


    $('#guardar').click(function () {
        guardar();
    });

    /**
     * Realiza la consulta al servidor para borrar un Evento existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID del Evento a borrar.
     * @param urlBorrarEvento {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function borrar(boton) {
        var pk = $(boton).attr('id').match(/[0-9]+/);
        var respuesta = confirm("¿Está seguro que deasea eliminar el evento?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarEvento,
                data: 'evento=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                Admin.manejarRespuestaServidor(json);
            });
        }
    }

    /**
     * Realiza la consulta al servidor para agregar un nuevo Evento.
     *
     * @method guardar
     * @param urlAgregarEvento {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';
        var fecha = $('#fecha_hora').val();

        if (jQuery.browser.mobile) {
            contenido = $('#evento_contenido').val();
        } else {
            contenido = ckeditor.getData();
        }

        $('#progress-principal').show();

        $('#portada').upload(urlAgregarEvento, {
            'titulo': titulo,
            'contenido': contenido,
            'fecha': fecha,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            Admin.manejarRespuestaServidor(JSON.stringify(json));
            $('#progress-principal').hide();
        }, function (progress, value) {
            $('#progress-principal > span').width(value + '%');
        });
    }

    $('#fecha_hora').datetimepicker({
        lang: 'es',
        format: 'd-m-Y H:i'
    });
});