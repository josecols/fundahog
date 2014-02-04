/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/

window.onload = function () {
    var html = CKEDITOR.replace('evento_contenido');

    $('.borrar').click(function () {
        borrar(this);
    });


    $('#guardar').click(function () {
        guardar();
    });

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
                manejarRespuestaServidor(json);
            });
        }
    }


    function guardar() {
        var titulo = $('input[name="titulo"]').val();
        var contenido = '';
        var fecha = $('#fecha_hora').val();

        if (jQuery.browser.mobile) {
            contenido = $('#evento_contenido').val();
        } else {
            contenido = html.getData();
        }

        $('#portada').upload(urlAgregarEvento, {
            'titulo': titulo,
            'contenido': contenido,
            'fecha': fecha,
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            console.log(json);
            manejarRespuestaServidor(JSON.stringify(json));
        });
    }

    $('#fecha_hora').datetimepicker({
        lang: 'es',
        format: 'd-m-Y H:i'
    });
}