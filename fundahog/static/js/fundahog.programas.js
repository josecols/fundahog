/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar la Programas.
 * @class Programas
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
    ckeditor = CKEDITOR.replace('programa_contenido');

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
     * Realiza la consulta al servidor para borrar un Programa existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID del programa a borrar.
     * @param urlBorrarPrograma {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function borrar(boton) {
        var pk = $(boton).attr('id').match(/[0-9]+/);
        var respuesta = confirm("¿Está seguro que deasea eliminar el programa?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarPrograma,
                data: 'programa=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                Admin.manejarRespuestaServidor(json);
            });
        }
    }

    /**
     * Realiza la consulta al servidor para agregar un nuevo Programa.
     *
     * @method guardar
     * @param urlAgregarSeccion {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';
        var elementos = ('' === $('#archivo').val() ? '#portada' : '.archivo');

        if (jQuery.browser.mobile) {
            contenido = $('#programa_contenido').val();
        } else {
            contenido = ckeditor.getData();
        }

        $('#progress-principal').show();

        $(elementos).upload(urlAgregarPrograma, {
            'titulo': titulo,
            'contenido': contenido,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            Admin.manejarRespuestaServidor(JSON.stringify(json));
            $('#progress-principal').hide();
        }, function (progress, value) {
            $('#progress-principal > span').width(value + '%');
        });
    }
});