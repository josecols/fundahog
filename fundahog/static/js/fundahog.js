/*  FUNDAHOG
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/
$(document).ready(function () {
    $('#menu').click(function () {
        $('#barra').slideToggle('fast');
    });
    $('.contenedor-input input').focusin(function () {
        $(this).parent().addClass('focus');
    });
    $('.contenedor-input input').focusout(function () {
        $(this).parent().removeClass('focus');
    });

    if ($('#importante').length > 0) {
        setTimeout(function () {
            $('#importante').slideToggle('slow', function () {
                $(this).css('display', 'block');
            });
        }, 2000);
    }
});