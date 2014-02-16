/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar Entradas y Categorías.
 * @class Blog
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
    ckeditor = CKEDITOR.replace('entrada_contenido');
    var nueva_categoria = $('#nueva_categoria');

    $('#nuevo').click(function () {
        $('.formulario.admin').slideToggle('fast');
        $("html, body").animate({
            scrollTop: 0
        }, "slow");
        $('#guardar').toggle();
    });

    $('#guardar').click(function () {
        guardar();
    });

    $('#agregar').click(function () {
        nueva_categoria.prop('contentEditable', 'true');
        nueva_categoria.slideToggle('fast');
        nueva_categoria.focus();
        nueva_categoria.text('');
        nueva_categoria.bind('keypress', function (e) {
            if (e.which == 13) {
                if (nueva_categoria.text() == nueva_categoria.data('categoria'))
                    return false;
                nueva_categoria.data('categoria', nueva_categoria.text());
                nueva_categoria.css('display', 'none');
                agregarCategoria(nueva_categoria.text());
            }
        });
    });

    $('.borrar').click(function () {
        borrar(this);
    });

    /**
     * Realiza la consulta al servidor para agregar una nueva Entrada.
     *
     * @method guardar
     * @param urlAgregarEntrada {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';
        var categorias = $('select[name="categorias"]').val() ? $('select[name="categorias"]').val().join(',') : '';
        var importante = ($('input[name=importante]').is(':checked') ? 'True' : 'False');
        if (jQuery.browser.mobile) {
            contenido = $('#entrada_contenido').val();
        } else {
            contenido = encodeURIComponent(ckeditor.getData());
        }

        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAgregarEntrada,
            data: 'titulo=' + titulo + '&contenido=' + contenido + '&categorias=' + categorias + '&importante=' + importante + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            Admin.manejarRespuestaServidor(json);
        });
    }

    /**
     * Realiza la consulta al servidor para agregar una nueva Categoría.
     *
     * @method agregarCategoria
     * @param categoria {String} Descripción de la categoría a agregar.
     * @param urlAgregarCategoria {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function agregarCategoria(categoria) {
        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAgregarCategoria,
            data: 'descripcion=' + categoria + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            Admin.manejarRespuestaServidor(json);
            json = JSON.parse(json);
            if (-1 != json.flag && json.data) {
                $('select[name="categorias"]').prepend('<option value="' + json.data + '">' + categoria + '</option>');
                $('.categorias ul').prepend('<li><a class="categoria" href="javascript:void(0)"><i class="fa fa-bookmark"></i>' + categoria + '</a></li>');
            }
        });
    }

    /**
     * Realiza la consulta al servidor para borrar una Entrada existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID de la Entrada a borrar.
     * @param urlBorrarEntrada {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function borrar(boton) {
        var pk = $(boton).attr('id').match(/[0-9]+/);
        var respuesta = confirm("¿Está seguro que deasea eliminar la entrada?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarEntrada,
                data: 'entrada=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                Admin.manejarRespuestaServidor(json);
            });
        }
    }
});