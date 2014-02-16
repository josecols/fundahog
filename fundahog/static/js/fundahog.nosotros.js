/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar la sección Nosotros. Representa además, un modelo para administrar cualquier sección.
 * @class Nosotros
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
    ckeditor = CKEDITOR.replace('seccion_contenido');

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
     * Realiza la consulta al servidor para borrar una Subsección existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID de la subsección a borrar.
     * @param urlBorrarSeccion {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function borrar(boton) {
        var pk = $(boton).attr('id').match(/[0-9]+/);
        var respuesta = confirm("¿Está seguro que deasea eliminar la sección?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarSeccion,
                data: 'seccion=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                Admin.manejarRespuestaServidor(json);
            });
        }
    }

    /**
     * Realiza la consulta al servidor para agregar una nueva Subsección a la sección Nosotros.
     *
     * @method guardar
     * @param urlAgregarSeccion {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar() {
        var superseccion = parseInt(superSeccion);
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';

        if (jQuery.browser.mobile) {
            contenido = $('#seccion_contenido').val();
        } else {
            contenido = ckeditor.getData();
        }

        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAgregarSeccion,
            data: 'titulo=' + titulo + '&contenido=' + contenido + '&superseccion=' + superSeccion + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            Admin.manejarRespuestaServidor(json);
        });
    }
});