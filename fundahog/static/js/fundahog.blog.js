/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/

ckeditor = null;
inline = false;

$(document).ready(function () {
    ckeditor = CKEDITOR.replace('entrada_contenido');
    var nueva_categoria = $('#nueva_categoria');

    $('#nuevo').click(function () {
        $('#nueva_categoria').prop('contentEditable', 'true')
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


    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';
        var categorias = $('select[name="categorias"]').val() ? $('select[name="categorias"]').val().join(',') : '';

        if (jQuery.browser.mobile) {
            contenido = $('#entrada_contenido').val();
        } else {
            contenido = encodeURIComponent(ckeditor.getData());
        }

        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAgregarEntrada,
            data: 'titulo=' + titulo + '&contenido=' + contenido + '&categorias=' + categorias + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            manejarRespuestaServidor(json);
        });
    }

    function agregarCategoria(categoria) {
        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAgregarCategoria,
            data: 'descripcion=' + categoria + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            manejarRespuestaServidor(json);
            if (-1 != json.flag && json.data) {
                $('select[name="categorias"]').prepend('<option value="' + json.data + '">' + categoria + '</option>');
                $('.categorias ul').prepend('<li><a class="categoria" href="javascript:void(0)"><i class="fa fa-bookmark"></i>' + categoria + '</a></li>');
            }
        });
    }

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
                manejarRespuestaServidor(json);
            });
        }
    }
});