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
        //inputTooShort: function (e) {
            // var t = e.minimum - e.input.length;
            // return "Ingresa " + t + " caractéres para buscar";
        // }
    }
});


function GetCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today;
}

function load_data() {
    var url = $('#ordenPagoForm').attr("data-proveedor-url");
    var tipo = $("#id_tipo_proveedor").val();
    if (tipo != "") {
        $("#div_razon-nombre").removeClass('d-none');
        $("#div_ruc-ci").removeClass('d-none');
        $.ajax({
            url: url,
            data: {
                'tipo': tipo
            },
            success: function (data) {
                $("#ruc_ci").html(data.ruc_ci);
                $("#razon_nombre").html(data.razon_nombre);
                $('#ruc_ci').val($('#id_proveedor').val()).trigger('change.select2');
                $('#razon_nombre').val($('#id_proveedor').val()).trigger('change.select2');
            }
        });

        if (tipo == "Natural") {
            $('label[for="ruc_ci"]').text('CI');
            $('label[for="razon_nombre"]').text('Nombre');
        }
        else if (tipo == "Jurídica") {
            $('label[for="ruc_ci"]').text('RUC');
            $('label[for="razon_nombre"]').text('Razón Social');
        }
    }
    else {
        $("#div_razon-nombre").addClass('d-none');
        $("#div_ruc-ci").addClass('d-none');
        $("#id_proveedor").val(null);
    }
};

function autocomplete(from, to) {
    if (from.val() != "") {
        $('#' + to).val(from.val()).trigger('change.select2');
    }
    else {
        $('#' + to).val(null).trigger('change.select2');
    }
}

function load_data_eventos() {
    var url = $('#ordenPagoForm').attr("data-evento-url");
    $.ajax({
        url: url,
        success: function (data) {
            $("#codigo_evento").html(data.codigo);
            $("#nombre_evento").html(data.nombre);
            $('#codigo_evento').val($('#id_evento').val()).trigger('change.select2');
            $('#nombre_evento').val($('#id_evento').val()).trigger('change.select2');
            console.log("Entre");
            
        }
    });
};

function load_data_descripcion() {
    var url = $('#ordenPagoForm').attr("data-tipo-url");
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


$("#id_tipo_proveedor").on("change", function (e) {
    $("#id_proveedor").val(null);
    load_data();
});

$('#razon_nombre').on('change', function () {
    autocomplete($(this), 'ruc_ci');
    $("#id_proveedor").val($('#ruc_ci').val());
})

$('#ruc_ci').on('change', function () {
    autocomplete($(this), 'razon_nombre');
    $("#id_proveedor").val($('#ruc_ci').val());
})


$(document).on('change', '#nombre_evento', function () {
    autocomplete($(this), 'codigo_evento');
    $("#id_evento").val($('#codigo_evento').val());
});

$(document).on('change', '#codigo_evento', function () {
    autocomplete($(this), 'nombre_evento');
    $("#id_evento").val($(this).val());
});

$(document).on('change', '#id_centro_costos', function (e) {
    load_data_descripcion();
    $("#id_egreso").val(null);
});


$(document).on('change', '#codigo', function () {
    autocomplete($(this), 'partida');
    $("#id_egreso").val($(this).val());
});

$(document).on('change', '#partida', function () {
    autocomplete($(this), 'codigo');
    $("#id_egreso").val($('#codigo').val());
});

$(document).ready(function (e) {
    load_data();
    load_data_eventos();
    load_data_descripcion();
    $(".file input[type='checkbox']").addClass('d-none');
    $(".file label[for^='ordenpagofile_set']").addClass('d-none');
    $(".currency-wrap input").addClass('text-right');
    $(".currency-wrap input").each(function (e) {
        $(this).val(formatNumber($(this).val()));
    })
});

$("#id_subtotal").change(function (e) {
    var valor = unformatNumber($(this).val());
    var iva = $("#id_iva").prop('checked') ? 0.12 : 0.00;
    var valor_iva = valor * iva;
    var otros = +unformatNumber($("#id_otros_cargos").val());
    var total = (valor * (1 + iva)) + otros;
    $("#id_valor_iva").val(formatNumber(valor_iva));
    $("#id_total").val(formatNumber(total));
});

$("#id_iva").change(function (e) {
    $("#id_subtotal").trigger('change');
});

$("#id_otros_cargos").change(function (e) {
    $("#id_subtotal").trigger('change');
});

$("#enviar").click(function (e) {
    e.preventDefault();
    $(".currency-wrap input").each(function (e) {
        $(this).val(unformatNumber($(this).val()));
    })
    $("form").trigger("submit");
})

$('#env-sol').click(function (e) {
    e.preventDefault();
    $("#id_estado").val("Enviado");
    $('#id_fecha_envio').val(GetCurrentDate());
    $(".currency-wrap input").each(function (e) {
        $(this).val(unformatNumber($(this).val()));
    })
    $("form").trigger("submit");
});

var n_form = 0;

function SetNum(value) {

    for (let index = 0; index < +(value) + 1; index++) {
        AddForm(index)
        n_form++;
    }
    $("#id_ordenpagofile_set-TOTAL_FORMS").val(n_form-1);
}

$("input:file").change(function (e) {
    if ($(this).val() == "") {
        if ($($(this).parent().children()[0]).attr("href") == null) {
            n_form--;
            RemoveForm(n_form);
        }
    }
    else {
        if ($(".formset:not('.d-none'):last input:file").val() != "") {
            AddForm(n_form);
            n_form++;
        }
    }
    $("#id_ordenpagofile_set-TOTAL_FORMS").val(n_form-1);
});

function AddForm(index) {
    $('.formset').eq(index).removeClass('d-none');
}

function RemoveForm(index) {
    $('.formset').eq(index).addClass('d-none');
}