
$(document).ready(function () {
    initSelect2();
    load_data_descripcion();
    load_data_producto();
});

$(document).on('change', "#id_unidad_medida", function (e) {
    $("#unidad_medida").val($(this).val());
});

$(document).on('change', "#id_costo_unitario", function (e) {
    $("#id_cantidad_anual").trigger('change');
});

$(document).on('change', "#id_iva", function (e) {
    $("#iva").val($(this).prop('checked'));
    $("#id_cantidad_anual").trigger('change');
});

$(document).on('change', '#id_centro_costos', function (e) {
    load_data_descripcion();
});

$(document).on('change', '#codigo', function () {
    autocomplete($(this), 'partida');
    $("#id_egreso").val($(this).val());
});

$(document).on('change', '#partida', function () {
    autocomplete($(this), 'codigo');
    $("#id_egreso").val($('#codigo').val());
});

$(document).on('change', '#id_tipo_compra', function (e) {
    $("#id_costo_unitario").val('0.00');
    load_data_producto();
    $("#id_cantidad_anual").trigger('change');
});

$(document).on('change', '#select-descripcion select', function () {
    $("#id_producto").val($(this).val());
    var prod = $(this).children('option[value="' + $(this).val() + '"]');
    $("#id_unidad_medida").val(prod.attr('data-unidad'));
    
    $("#unidad_medida").val(prod.attr('data-unidad'));
    $("#id_iva").prop('checked', prod.attr('data-iva') == "True" ? true : false);
    $("#iva").val($("#id_iva").prop('checked'));
    $("#id_cantidad_anual").trigger('change');
});


$(document).on('change', "#id_cantidad_anual", function () {
    var cant = +$(this).val();
    var unitario = unformatNumber($("#id_costo_unitario").val());
    var subtotal = cant * unitario;
    //Si iva es un check....
    var iva = $("#id_iva").prop('checked') ? 1.12 : 1;
    var total = subtotal * iva;
    $("#id_subtotal").val(formatNumber(subtotal));
    $("#id_total").val(formatNumber(total));
});

$(document).on('click', "#pnuevo", function () {
    $('#select-descripcion select').select2('close');
})

$(document).on('focus', "#select-descripcion span.selection", function (e) {
    load_data_producto();
});

function initSelect2() {
    initSelect2Partida();
    initSelect2Suministros();
}

function initSelect2Partida() {
    $('.select2').select2({
        dropdownParent: $('#productoModalCenter'),
        dropdownAutoWidth: true,
        width: '100%',
        // minimumInputLength: 2,
        language: {
            noResults: function () {
                return "No hay resultados";
            },
            searching: function () {
                return "Buscando...";
            },
            // inputTooShort: function (e) {
            //     var t = e.minimum - e.input.length;
            //     return "Ingresa " + t + " caractéres para buscar";
            // }
        }
    });
}

function initSelect2Suministros() {
    $('#select-descripcion select').select2({
        dropdownParent: $('#productoModalCenter'),
        dropdownAutoWidth: true,
        width: '100%',
        minimumInputLength: 1,
        language: {
            noResults: function () {
                var url = $('#form').attr('data-suministro');
                $(".select2-results__options").append("<a id='pnuevo' class='btn btn-secondary btn-sm' href='" + url + "' target='_blank'>Agregar Nuevo</a>");
                return "No hay resultados";
            },
            searching: function () {
                return "Buscando...";
            },
            inputTooShort: function (e) {
                var t = e.minimum - e.input.length;
                return "Ingresa " + t + " caractéres para buscar";
            }
        }
    });
}


function load_data_descripcion() {
    var url = $('#form').attr("data-tipo-url");
    var tipo = $("#id_centro_costos").val();
    if (tipo != "") {
        $.ajax({
            url: url,
            data: {
                'tipo': tipo
            },
            success: function (data) {
                $("#codigo").html(data.codigo);
                $("#codigo").val($("#id_egreso").val()).trigger('change.select2');
                $("#partida").html(data.partida);
                $("#partida").val($("#id_egreso").val()).trigger('change.select2');
            }
        });
    }
    else {
        $('#codigo').val(null).trigger('change.select2');
        $('#partida').val(null).trigger('change.select2');
    }
};


function load_data_producto() {
    var url = $('#form').attr("data-producto-url");
    var tipo = $("#id_tipo_compra").val();

    if (tipo === "Suministro") {
        $("#select-descripcion").removeClass('d-none');
        $("#id_descripcion").addClass('d-none');
        $("#id_unidad_medida").attr('disabled', true);
        $("#id_iva").attr('disabled', true);
        $("#id_descripcion").val(null);
        $.ajax({
            url: url,
            success: function (data) {
                $("#select-descripcion select").html(data.producto);
                $("#select-descripcion select").val($("#id_producto").val()).trigger('change');
            }
        });
    }
    else {
        $("#select-descripcion").addClass('d-none');
        $('#select-descripcion select').val(null).trigger('change.select2');
        $("#id_producto").val(null);
        $("#id_iva").attr('disabled', true).prop('checked', false);
        $("#id_descripcion").removeClass('d-none');
        $("#id_iva").prop('checked', $("#iva").val() == "True" ? true : false);
        if (tipo === "Bien") {
            $("#id_unidad_medida").attr('disabled', false);
            $("#id_iva").attr('disabled', false);
        }
        else if (tipo == "Servicio") {
            $("#id_unidad_medida").attr('disabled', true).val('Ninguno').trigger('change');
            $("#id_iva").attr('disabled', false);
        }
    }
};

//Autocompleta de un select a otro usando el id
function autocomplete(from, to) {
    if (from.val() != "") {
        $('#' + to).val(from.val()).trigger('change.select2');
    }
    else {
        $('#' + to).val(null).trigger('change.select2');
    }
}

function GetCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today;
}