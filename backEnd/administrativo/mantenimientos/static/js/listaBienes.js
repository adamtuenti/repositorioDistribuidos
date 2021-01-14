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
    var url = $('#mantenimientoForm').attr("data-bien-url");
    var tipo = $("#id_tipo_bien").val();
    if (tipo != "") {
        $("#div_cod_Inventariound").removeClass('d-none');
        $("#div_cod_bien").removeClass('d-none');
        $("#div_nombre").removeClass('d-none');
        $.ajax({
            url: url,
            data: {
                'tipo_Bien': tipo
            },
            success: function (data) {
                $("#cod_Inventariound").html(data.cod_Inventariound);
                $("#cod_bien").html(data.cod_bien);
                $("#nombre").html(data.nombre);
                $('#cod_Inventariound').val($('#id_bien').val()).trigger('change.select2');
                $('#cod_bien').val($('#id_bien').val()).trigger('change.select2');
                $('#nombre').val($('#id_bien').val()).trigger('change.select2');
            }
        });

    }
    else {
        $("#div_cod_Inventariound").addClass('d-none');
        $("#div_cod_bien").addClass('d-none');
        $("#div_nombre").addClass('d-none');
        $("#id_bien").val(null);
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

function load_data_descripcion() {
    var url = $('#mantenimientoForm').attr("data-bienInd-url");
    var bien = $("#id_bien").val();
    if (bien != "") {
        $.ajax({
            url: url,
            data: {
                'id_bien': bien
            },
            success: function (data) {
                $("#tipo_mantenimiento").val(data.tipo_mantenimiento);
                $("#freq_mantenimiento").val(data.freq_mantenimiento);
            }
        });
    }
    else {
        $('#tipo_mantenimiento').val(null).trigger('change.select2');
        $('#freq_mantenimiento').val(null).trigger('change.select2');
    }
};

function load_data_ingreso() {
    var url1 = $('#mantenimientoForm').attr("data-ingresoBienes-url");
    var url2 = $('#mantenimientoForm').attr("data-ingresoBienesId-url");
    var num_factura = $("#num_factura").val();
    var id_ingreso = $("#id_ingreso_bien").val();
    if (num_factura != "") {
        $.ajax({
            url: url1,
            data: {
                'num_factura': num_factura
            },
            success: function (data) {
                $("#fecha_facturacion").val(data.fecha_facturacion);
                $("#centro_costos").val(data.centro_costos);
                $("#cod_orden").val(data.cod_orden);
                $("#id_ingreso_bien").val(data.id_ingreso);
            }
        });
    }
    else if (id_ingreso != "" && $("#cod_orden").val() == "") {
        $.ajax({
            url: url2,
            data: {
                'id_ingreso': id_ingreso
            },
            success: function (data) {
                $("#fecha_facturacion").val(data.fecha_facturacion);
                $("#centro_costos").val(data.centro_costos);
                $("#cod_orden").val(data.cod_orden);
                $("#num_factura").val(data.num_factura);
                //console.log(data.ruc_ci, $("select2-ruc-container").val() );
            }
        });
    }
    else {
        $("#fecha_facturacion").val(null).trigger('change.select2');
        $('#cod_orden').val(null).trigger('change.select2');
        $('#centro_costos').val(null).trigger('change.select2');
        $("#id_ingreso_bien").val(null).trigger('change.select2');
    }
};

function load_costos() {
    $("#sub_total").val($("#id_subtotal").val());
    $("#iva").val($("#id_valor_iva").val());
    $("#descuento").val($("#id_descuento").val());
    $("#valor_total").val($("#id_total").val());
};

$("#num_factura").on("change", function (e) {
    load_data_ingreso();
});

$("#sub_total").on("change", function (e) {
    var valor =  parseFloat($(this).val());
    var iva = ($("#id_iva").val() == "True") ? 0.12 : 0.00;
    var valor_iva = valor * iva;
    $("#iva").val(valor_iva.toFixed(2));
    var descuento = parseFloat($("#descuento").val());
    var total = (valor+valor_iva-descuento).toFixed(2)
    $("#valor_total").val(total);

    $("#sub_total").val(valor);
    $("#id_subtotal").val(valor);
    $("#id_valor_iva").val(valor_iva.toFixed(2));
    $("#id_descuento").val(descuento);
    $("#id_total").val(total);
});

$("#descuento").on("change", function (e) {
    $("#sub_total").trigger('change');
});

$("#id_tipo_bien").on("change", function (e) {
    $("#id_bien").val(null).trigger('change');
    load_data();
});

$('#cod_Inventariound').on('change', function () {
    autocomplete($(this), 'cod_bien');
    autocomplete($(this), 'nombre');
    $("#id_bien").val($('#cod_bien').val()).trigger('change');
})

$('#cod_bien').on('change', function () {
    autocomplete($(this), 'cod_Inventariound');
    autocomplete($(this), 'nombre');
    $("#id_bien").val($('#cod_Inventariound').val()).trigger('change');
})

$('#nombre').on('change', function () {
    autocomplete($(this), 'cod_Inventariound');
    autocomplete($(this), 'cod_bien');
    $("#id_bien").val($('#cod_Inventariound').val()).trigger('change');
})

$("#id_bien").change(function(){
    load_data_descripcion();
});

$(document).ready(function (e) {
    load_data();
    load_data_ingreso();
    load_data_descripcion();
    load_costos();
});

$("#id_iva").change(function (e) {
    $("#sub_total").trigger('change');
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