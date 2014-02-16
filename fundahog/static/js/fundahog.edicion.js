/*  FUNDAHOG
 *    UCAB Guayana
 *    Aplicación: FUNDAHOG WEB
 *    Autor: Jose Cols - josecolsg@gmail.com - @josecols
 *    Version: 1.0
 */

/**
 * Este módulo controla las vistas con edición inline.
 * @class Edicion
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

    /**
     * En el caso de que ocurran cambios al texto los refleja en la interfaz ofreciendo la opción de Guardar cambios.
     *
     * @method cambios
     **/
    function cambios() {
        $('#guardar').html('<i class="fa fa-floppy-o"></i>Guardar cambios');
        $('#guardar').addClass('cambios');
        guardar = true;
    }

    /**
     * Realiza la consulta al servidor para modificar la tabla correspondiente.
     *
     * @method modificar
     * @param url {String} Dirección de la vista en el servidor. Este parámetro debe estar definido global y estáticamente en el template.
     * @param data {String} Datos que serán enviados al servidor, incluye csrfToken. Este parámetro debe estar definido global y estáticamente en el template.
     **/
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
                Admin.manejarRespuestaServidor(data);
            });
        }
    }
});