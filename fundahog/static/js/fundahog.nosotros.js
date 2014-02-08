/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/

ckeditor = null;
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
                manejarRespuestaServidor(json);
            });
        }
    }

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
            manejarRespuestaServidor(json);
        });
    }
});