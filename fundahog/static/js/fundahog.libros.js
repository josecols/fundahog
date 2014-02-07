/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
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
            manejarRespuestaServidor(JSON.stringify(json));
            $('#progress').hide();
        }, function (progress, value) {
            $('#progress > span').width(value + '%');
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
            json = JSON.parse(json);
            if (-1 != json.flag && json.data) {
                $('select[name="categorias"]').prepend('<option value="' + json.data + '">' + categoria + '</option>');
                $('.categorias ul').prepend('<li><a class="categoria" href="javascript:void(0)"><i class="fa fa-bookmark"></i>' + categoria + '</a></li>');
            }
        });
    }

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
                manejarRespuestaServidor(json);
            });
        }
    }
});