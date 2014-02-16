/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Módulo modal que permite agregar imágenes al contenido y realizar cargas a los álbumes de distintas galerías.
 * @class Selector
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
    if (jQuery.browser.mobile && !inline) {
        $('.pop.fancybox').hide();
    }
    $('.pop.fancybox').click(function () {
        cargarGalerias();
    });


    $('#galerias').change(function () {
        cargarAlbumes(this);
    });

    $('#albumes').change(function () {
        cargarImagenes(this);
    });

    $('#imagen').change(function () {
        agregarImagen(this);
    });

    $(document).on('click', '.imagen', function () {
        if (inline) {
            $('#contenido-html').prepend('<img alt="' + $(this).attr('data-titulo') + '" src=' + $(this).attr('data-url') + '/>');
            $('div[contenteditable]').change();
        } else {
            ckeditor.insertHtml('<img alt="' + $(this).attr('data-titulo') + '" src=' + $(this).attr('data-url') + '/>');
        }
    });

    /**
     * Realiza la consulta al servidor para listar todas las Galerías existentes.
     *
     * @method cargarGalerias
     * @param urlGalerias {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function cargarGalerias() {
        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlGalerias,
            data: 'csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            json = JSON.parse(json);
            var html = '';

            json.data.forEach(function (galeria) {
                html += '<option value="' + galeria.id + '">' + galeria.titulo + '</option>';
            });

            $('#galerias').html(html);
            $('#galerias').change();
        });
        $('.fancybox').fancybox();
    }

    /**
     * Realiza la consulta al servidor para listar todos los Álbumes existentes en la galería seleccionada.
     *
     * @method cargarAlbumes
     * @param galerias {Object} Select que contiene la lista de todas las galerías.
     * @param urlAlbumes {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function cargarAlbumes(galerias) {
        var galeria = parseInt($(galerias).val());
        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlAlbumes,
            data: 'galeria=' + galeria + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            json = JSON.parse(json);
            var html = '';

            json.data.forEach(function (album) {
                html += '<option value="' + album.id + '">' + album.titulo + '</option>';
            });

            $('#albumes').html(html);
            $('#albumes').change();
        });
    }

    /**
     * Realiza la consulta al servidor para listar todas las Imágenes existentes en el álbum seleccionado.
     *
     * @method cargarImagenes
     * @param albumes {Object} Select que contiene la lista de todos los álbumes.
     * @param urlImagenes {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function cargarImagenes(albumes) {
        var album = parseInt($(albumes).val());
        var request = $.ajax({
            async: true,
            type: 'POST',
            url: urlImagenes,
            data: 'album=' + album + '&csrfmiddlewaretoken=' + csrfToken,
            dataType: "text"
        });
        request.done(function (json) {
            json = JSON.parse(json);
            var html = '';

            json.data.forEach(function (imagen) {
                html += '<li data-titulo="' + imagen.titulo + '" data-url=' + imagen.imagen + ' class="imagen" style="background-image: url(' + mediaURL + imagen.thumbnail + ');"></li>';
            });
            $('.imagenes').html(html + '<div class="fix"></div>');
            $('.fancybox-inner').css('height', 'auto');
        });
    }

    /**
     * Realiza la consulta al servidor para agregar una nueva Imagen al álbum seleccionado.
     *
     * @method agregarImagen
     * @param urlAgregarImagen {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param csrfToken {String} Código para evitar falsificación de peticiones. Este parámetro debe estar definido global y estáticamente en el template.
     **/
    function agregarImagen(input) {
        var titulo;
        if ('' === (titulo = $('#titulo_imagen').val()))
            titulo = pseudoUUID();

        $('#progress').show();

        $(input).upload(urlAgregarImagen, {
            'titulo': titulo,
            'album': $('#albumes').val(),
            'csrfmiddlewaretoken': csrfToken
        }, function (json) {
            if (0 === json.flag) {
                $('#albumes').change();
                $('#progress').hide();
            } else {
                var mensaje = '';
                for (key in json.errores) {
                    mensaje += 'Ha ocurrido un error con ' + Admin.capitalizarInicial(key) + ': ' + json.errores[key][0] + ' ';
                }
                alert(mensaje);
            }
        }, function (progress, value) {
            $('#progress > span').width(value + '%');
        });
    }
});