/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo ofrece las herramientas administrativas al cliente para gestionar Libros y Categorías de libros.
 * @class Libros
 */

$(document).ready(function () {
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
     * Realiza la consulta al servidor para agregar un nuevo Libro.
     *
     * @method guardar
     * @param urlAgregarLibro {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var descripcion = $('textarea[name="descripcion"]').val();
        var categorias = $('select[name="categorias"]').val() ? $('select[name="categorias"]').val().join(',') : '';

        $('#progress').show();

        $('.archivo').upload(urlAgregarLibro, {
            'titulo': titulo,
            'descripcion': descripcion,
            'categorias': categorias,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            Admin.manejarRespuestaServidor(JSON.stringify(json));
            $('#progress').hide();
        }, function (progress, value) {
            $('#progress > span').width(value + '%');
        });
    }

    /**
     * Realiza la consulta al servidor para agregar una nueva Categoría de libro.
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
     * Realiza la consulta al servidor para borrar un libro existente.
     *
     * @method borrar
     * @param boton {Object} Botón que dispara el evento y que contiene el ID del Libro a borrar.
     * @param urlBorrarLibro {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function borrar(boton) {
        var pk = $(boton).attr('id').match(/[0-9]+/);
        var respuesta = confirm("¿Está seguro que deasea eliminar el libro?");

        if (respuesta == true) {
            var request = $.ajax({
                async: true,
                type: 'POST',
                url: urlBorrarLibro,
                data: 'libro=' + pk + '&csrfmiddlewaretoken=' + csrfToken,
                dataType: "text"
            });
            request.done(function (json) {
                Admin.manejarRespuestaServidor(json);
            });
        }
    }
});