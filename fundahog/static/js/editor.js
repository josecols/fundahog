/*  Editor
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/
$(document).ready(function () {
	$("div[contenteditable='true']").bind('input', function() {
		$('#guardar').text('Guardar cambios');
		$('#guardar').addClass('cambios');
	});
});