/*  CKEDITOR INIT
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/
$(document).ready(function () {
	$('#entrada').click(function (){
		$('.formulario.entrada').slideToggle('slow');
		$("html, body").animate({ scrollTop: 0 }, "slow");
		$('#guardar').toggle();
	});
});	