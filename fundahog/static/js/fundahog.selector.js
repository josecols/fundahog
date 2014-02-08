/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
    Selector de imágenes para CKEditor
*/
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
    });

    $('#galerias').change(function () {
        var galeria = parseInt($(this).val());
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
    });

    $('#albumes').change(function () {
        var album = parseInt($(this).val());
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
    });

    $('#imagen').change(function () {
        var titulo;
        if ('' === (titulo = $('#titulo_imagen').val()))
            titulo = pseudoUUID();

        $('#progress').show();

        $(this).upload(urlAgregarImagen, {
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
                    mensaje += 'Ha ocurrido un error con ' + capitalizarInicial(key) + ': ' + json.errores[key][0] + ' ';
                }
                alert(mensaje);
            }
        }, function (progress, value) {
            $('#progress > span').width(value + '%');
        });
    });

    $(document).on('click', '.imagen', function () {
        if (inline) {
            $('#contenido-html').prepend('<img alt="' + $(this).attr('data-titulo') + '" src=' + $(this).attr('data-url') + '/>');
            $('div[contenteditable]').change();
        } else {
            ckeditor.insertHtml('<img alt="' + $(this).attr('data-titulo') + '" src=' + $(this).attr('data-url') + '/>');
        }
    });
});