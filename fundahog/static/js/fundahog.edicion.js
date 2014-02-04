/*  CKEDITOR INIT
    UCAB Guayana
    Aplicación: FUNDAHOG WEB
    Autor: Jose Cols - josecolsg@gmail.com - @josecols
    Version: 1.0
*/
$(document).ready(function () {
    var guardar = false;

    $('div[contenteditable]').on('focus', function () {
        var $this = $(this);
        $this.data('before', $this.html());
        return $this;
    }).on('blur input paste', function () {
        var $this = $(this);
        if ($this.data('before') !== $this.html()) {
            $this.data('before', $this.html());
            $this.trigger('change');
        }
        return $this;
    });

    $("div[contenteditable='true']").bind('change', function () {
        cambios();
    });

    $('#guardar').click(function () {
        modificar();
    });

    function cambios() {
        $('#guardar').html('<i class="fa fa-floppy-o"></i>Guardar cambios');
        $('#guardar').addClass('cambios');
        guardar = true;
    }

    function modificar() {
        if (guardar) {
            var request = $.ajax({
                async: true,
                type: "POST",
                url: url,
                data: data,
                dataType: "text"
            });
            request.done(function (data) {
                manejarRespuestaServidor(data);
            });
        }
    }
});