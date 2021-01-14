$('.select2').select2({
    width: '100%',
    //minimumInputLength: 1,
    language: {

        noResults: function () {
            return "No hay resultados";
        },
        searching: function () {

            return "Buscando...";
        },

    }
});

function load_data() {
    var url = $('#mantenimientoForm').attr("data-proveedor-url");
        $.ajax({
            url: url,
            data: {
                
            },
            success: function (data) {
                $("#ruc").html(data.ruc_ci);
                $("#razon").html(data.razon_nombre);
                $('#ruc').val($('#id_proveedor').val()).trigger('change.select2');
                $('#razon').val($('#id_proveedor').val()).trigger('change.select2');
                console.log(data);
            }
        });
};

load_data();

function autocomplete(from, to) {
    if (from.val() != "") {
        $('#' + to).val(from.val()).trigger('change.select2');
    }
    else {
        $('#' + to).val(null).trigger('change.select2');
    }
}

$('#razon').on('change', function () {
    autocomplete($(this), 'ruc');
    $("#id_proveedor").val($('#ruc').val());
})

$('#ruc').on('change', function () {
    autocomplete($(this), 'razon');
    $("#id_proveedor").val($('#ruc').val());
})

$(document).ready(function (e) {
    load_data();
});