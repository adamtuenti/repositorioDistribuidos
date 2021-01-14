
var p_url = $('#form').attr("data-juridica-url");

$('.select2').select2({
    minimumInputLength: 2,
    language: {

        noResults: function () {
            $(".select2-results__options").append("<a id='pnuevo' class='btn btn-secondary btn-block btn-sm' href='" + p_url + "' target='_blank'>Agregar Nuevo</a>");
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

$('.select2-evento').select2({
    language: {

        noResults: function () {
            return "No hay resultados";
        },
        searching: function () {

            return "Buscando...";
        }
    }
});

function load_data(estado) {
    var url = $('#form').attr("data-persona-url");
    var persona = $("#id_tipo").val();
    if (persona != "") {
        $.ajax({
            url: url,
            data: {
                'persona': persona
            },
            success: function (data) {
                if (persona === "Jurídica") {
                    if (estado == 0) {
                        $("#id_ruc_ci").attr('disabled', false)
                        $("#id_razon_nombres").attr('disabled', false)
                    }
                    $("#id_ruc_ci").html(data.ruc_ci);
                    $("#id_razon_nombres").html(data.razon_nombre);
                    $('#id_ruc_ci').val($('input[name="ruc_ci"]').val()).trigger('change.select2');
                    $('#id_razon_nombres').val($('input[name="razon_nombres"]').val()).trigger('change.select2');
                }
                else {
                    $("#id_ruc_ci").attr('disabled', true)
                    $("#id_razon_nombres").attr('disabled', true)
                    $('#id_ruc_ci').val(null).trigger('change.select2');
                    $('#id_razon_nombres').val(null).trigger('change.select2');
                    $('input[name="ruc_ci"]').val(null);
                    $('input[name="razon_nombres"]').val(null);
                }
            }
        });
    }
    else {
        $("#id_ruc_ci").attr('disabled', true)
        $("#id_razon_nombres").attr('disabled', true)
        $('#id_ruc_ci').val(null).trigger('change.select2');
        $('#id_razon_nombres').val(null).trigger('change.select2');
        $('input[name="ruc_ci"]').val(null);
        $('input[name="razon_nombres"]').val(null);
    }
};

function load_data_eventos(estado) {
    var url = $('#form').attr("data-evento-url");
    if (estado =="Autorizada con evento" )
        url= $('#form').attr("data-evento-all-url");
    $.ajax({
        // data:{
        //     'tipo':$("#id_tipo").val()
        // },
        url: url,
        success: function (data) {
            $("#codigo_evento").html(data.codigo);
            $("#nombre_evento").html(data.nombre);
            $('#codigo_evento').val($('#id_evento').val()).trigger('change.select2');
            $('#nombre_evento').val($('#id_evento').val()).trigger('change.select2');
            $('#resumen_nombre_evento').val($('#nombre_evento option[value="' + $('#id_evento').val() + '"]').text())
            $("#modalidad_evento").val($('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-modalidad"));
            var finicio = $('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-finicio");
            var ffin = $('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-ffin");
            if(finicio==undefined || ffin==undefined) return;
            var ymd = finicio.split("/");
            $("#fecha_inicio_evento").val(ymd[2] + "-" + ymd[1] + "-" + ymd[0]);
            var ymd = ffin.split("/");
            $("#fecha_fin_evento").val(ymd[2] + "-" + ymd[1] + "-" + ymd[0]);
        }
    });
};



//Autocompleta de un select a otro usando el id
function autocomplete(from, to) {
    if (from.val() != "") {
        var valor = from.val();
        $('#' + to).val(valor).trigger('change.select2');
    }
    else {
        $('#' + to).val(null).trigger('change.select2');
    }
}

/**
 * Funcion para calcular los valores de ingresos
 */
function CalcularIngresos() {
    var valor_u = unformatNumber($("#id_ingreso_individual_sin_desc").val());
    var n_participantes = +$("#id_n_participantes").val();
    var sin_descuento_total = valor_u * n_participantes;
    var descuento_individual = +$("#id_descuento_maximo").val() / 100 * valor_u;
    var descuento_total = descuento_individual * n_participantes;
    var egresos = unformatNumber($('#id_total_egresos').val())
    var ingreso_total = sin_descuento_total - descuento_total;
    var utilidad = ingreso_total - egresos
    $('#id_utilidad').val(isNaN(utilidad) ? null : formatNumber(utilidad));
    var margen = (utilidad / ingreso_total * 100);
    $("#id_margen_contribucion").val(isNaN(margen) ? null : formatNumber(margen))
    $('#id_ingreso_total_sin_desc').val(formatNumber(sin_descuento_total));
    $('#id_descuento_individual').val(formatNumber(descuento_individual));
    $('#id_descuento_total').val(formatNumber(descuento_total));
    const ing_neto = valor_u - descuento_individual;
    $('#id_ingreso_neto_individual').val(formatNumber(ing_neto)).trigger('change');
    $('#provision_mejoras_unitario').val(formatNumber(ingreso_total));
    $('#resumen_precio_evento').val(formatNumber(ing_neto)).trigger('change');
    $('#id_ingreso_neto_total').val(formatNumber(ingreso_total));
    $('.total-impuesto').trigger('change');
    $('#resumen_ingreso').val(formatNumber(ingreso_total));
    $('#id_provision_mejoras_porcentaje').trigger('change');
    CalcularHonorarios();
}

/**
 * Funcion que hace un requerimiento ajax al servidor para obtener los valores unitarios del tarifario y calcular
 * @param {*} modelo Representa el nombre de la fk en el modelo de PresupuestoEvento
 * @param {*} id Represeta la pk de la fk del cual el valor se va a buscar
 */
function CargarInfo(modelo, id) {
    var url = $('form').attr("data-info-url");
    $.ajax({
        url: url,
        data: {
            'modelo': modelo,
            'id': id,
        },
        success: function (data) {
            $('#id_' + modelo + '_unitario').val(formatNumber(data.costo)).trigger('change');
        }
    })
}

function CargarAportacion(modelo, id) {
    var url = $('form').attr("data-info-url");
    $.ajax({
        url: url,
        data: {
            'modelo': modelo,
            'id': id,
        },
        success: function (data) {
            $("#id_aportacion_espol_porcentaje").val(+data.costo.espol).trigger('change')
            $("#id_aportacion_espoltech_porcentaje").val(+data.costo.espoltech).trigger('change')
            $("#id_aportacion_ministerio_porcentaje").val(+data.costo.ministerio).trigger('change')
            $("#id_aportacion_fundaespol_porcentaje").val(+data.costo.fundaespol).trigger('change')
        }
    })
}


function CalcularValoresEgresos(valor, id_total, dependodnother, id_field) {
    var valo1 = unformatNumber(valor);
    if (valor < 0) valo1 = 0;
    var valor2 = 1;
    if (dependodnother == "True") {
        valor2 = unformatNumber($("#" + id_field).val());
    }
    var resultado = +valo1 * +valor2;
    $("#" + id_total).val(formatNumber(resultado)).trigger('change');
}



function CalcularEgresos(clase) {
    var total = 0;
    $("." + clase).each(function (index) {
        if ($(this).val() !== "")
            total += +unformatNumber($(this).val());
    });
    return total;
}


function CalcularHonorarios() {
    var resultado = CalcularEgresos("total-impuesto");
    var resultado2 = CalcularEgresos('total-honorario');
    $("#id_honorario_total_evento").val(formatNumber(resultado)).trigger('change');
    $("#id_honorario_total_evento_impuesto").val(formatNumber(resultado2));
    var honorario = resultado2 / +unformatNumber($("#id_ingreso_neto_total").val()) * 100;
    if (isNaN(honorario) || !isFinite(honorario)) {
        honorario = 0;
    }
    $("#id_porcentaje_honorario_instructor").val(honorario.toFixed(0));
}

function DependenciaCalculo(lista_id) {
    $.each(lista_id, function (index, value) {
        $('#' + value).trigger('change');
    })
}

$('.otros').change(function (e) {
    if (+$(this).val() != 0) {
        $('#' + e.target.dataset.label).attr('readonly', false);
    }
    else {
        $('#' + e.target.dataset.label).attr('readonly', true);
    }
});


function CostoInstructores() {
    var costo_final = 0;
    var costo_instructores = '';
    $(".costo-hora").each(function (index) {
        if ($(this).val() !== "") {
            var val = +unformatNumber($(this).val());
            costo_final += val;
            costo_instructores += val + ',';
        }
    })

    $('#id_costo_instructores').val(formatNumber(costo_final));
    $('#id_costo_hora_instructores').val(costo_instructores);
    CalcularHonorarios();
}

function CostoImpuesto() {
    var impuesto_select = '';
    var impuesto_unitario = '';
    var impuesto_final = '';
    var horas_honorario = '';
    var porcentaje_honorario = '';
    var porcentaje_impuesto = '';

    $(".impuesto-select").each(function (index) {
        if ($(this).val() !== "") {
            impuesto_select += ($(this).prop('checked') ? 1 : 0) + ',';
        }
    })

    $(".total-honorario").each(function (index) {
        if ($(this).val() !== "") {
            impuesto_unitario += unformatNumber($(this).val()) + ',';
        }
    })

    $(".total-impuesto").each(function (index) {
        if ($(this).val() !== "") {
            impuesto_final += unformatNumber($(this).val()) + ',';
        }
    })

    $(".horas-honorario").each(function (index) {
        if ($(this).val() !== "") {
            horas_honorario += unformatNumber($(this).val()) + ',';
        }
    })

    $(".porcentaje-honorario").each(function (index) {
        if ($(this).val() !== "") {
            porcentaje_honorario += +$(this).val() + ',';
        }
        CalcularHonorarios();
    })

    $(".porcentaje-impuesto").each(function (index) {
        if ($(this).val() !== "") {
            porcentaje_impuesto += +$(this).val() + ',';
        }
    })

    $('#id_honorario_instructores').val(porcentaje_honorario);
    $('#id_horas_instructores').val(horas_honorario);
    $('#id_impuesto_select').val(impuesto_select);
    $('#id_valor_total').val(impuesto_unitario);
    $('#id_impuesto_total').val(impuesto_final);
    $('#id_impuesto_porcentaje').val(porcentaje_impuesto);
}


function GetCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    return today;
}

function CambiarEstado() {
    if ($("#codigo_evento").val() !== null && $("#codigo_evento").val() !== "" && $("#nombre_evento").val() !== null && $("#nombre_evento").val() !== "") {
        $("#id_estado").val("Autorizada con evento");
        $('#id_fecha_aprobada_con').val(GetCurrentDate());
    }
    else {
        $("#id_estado").val("Autorizada sin evento");
        $('#id_fecha_aprobada_con').val(null);
    }
}

$("#id_n_cursos").change(function (e) {
    var depend = ['id_pago_docente_unitario'];
    DependenciaCalculo(depend);
});

$("#id_n_horas").change(function (e) {
    var depend = ['id_instalaciones_unitario'];
    DependenciaCalculo(depend);
});

$("#id_n_dias").change(function (e) {
    var depend = ['id_movilizacion_interna_unitario', 'n_dias_participantes'];
    DependenciaCalculo(depend);
});

$("#id_ingreso_neto_individual").change(function (e) {
    var depend = ['id_aportacion_espol_porcentaje', 'id_aportacion_espoltech_porcentaje', 'id_aportacion_ministerio_porcentaje', 'id_aportacion_fundaespol_porcentaje', 'id_aportacion_facultad_porcentaje_unitario'];
    DependenciaCalculo(depend);
});

$('#id_aportacion_facultad_total').change(function (e) {
    $('#resumen_aporte_facultad').val(e.target.value);
    $('#id_n_cursos').trigger('change');
})

$("#id_n_participantes").change(function (e) {
    var depend = ['id_ingreso_individual_sin_desc', 'id_certificados_unitario', 'id_cd_unitario','id_carpeta_unitario', 'id_maletin_unitario', 'id_block_unitario', 'id_lapiz_unitario', 'id_pluma_unitario', 'n_dias_participantes',
        'id_credencial_pvc', 'id_credencial_plastico_unitario', 'id_pendrive_unitario','id_personal_evento_unitario','id_cd_unitario','id_otros_materiales_unitario', 'ceremonia_participantes', 'id_break_evento_dias', 
        'id_almuerzo_evento_dias','id_imprevisto_unitario', 'id_total_egresos'];
    $('#resumen_n_participantes').val(+$(this).val());
    DependenciaCalculo(depend);
});

$("#id_ingreso_individual_sin_desc").change(CalcularIngresos);

$("#ceremonia_participantes").change(function (event) {
    var n_participantes = +$('#id_n_participantes').val();
    var valor = +(+n_participantes * 2) + 5;
    event.target.value = valor;
    CalcularValoresEgresos(valor, event.target.dataset.total, event.target.dataset.depend, event.target.dataset.field);
});

$("#n_dias_participantes").change(function (event) {
    var n_participantes = +$('#id_n_participantes').val();
    var n_dias = +$('#id_n_dias').val();

    var valor = n_participantes * n_dias
    event.target.value = valor;
    CalcularValoresEgresos(+valor, event.target.dataset.total, event.target.dataset.depend, event.target.dataset.field);
});

$('#n_dias_participantes').change();

$(".valor-total").change(function (event) {
    CalcularValoresEgresos(event.target.value, event.target.dataset.total, event.target.dataset.depend, event.target.dataset.field);
});

$(".valor-porcentaje").change(function (event) {
    if (event.target.value > +event.target.max) {
        event.target.value = +event.target.max
    }
    if (event.target.value < +event.target.min) {
        event.target.value = +event.target.min
    }
    CalcularValoresEgresos(+(event.target.value / 100), event.target.dataset.total, event.target.dataset.depend, event.target.dataset.field);
});

$(".punto").change(function (event) {
    var egreso_fijo = unformatNumber($('#id_total_egresos_fijos').val());
    var precio = unformatNumber($('#id_ingreso_neto_individual').val());
    var egreso_unit = unformatNumber($("#id_egreso_variable_unit").val());
    var resultado = +egreso_fijo / +(precio - egreso_unit);
    if (+resultado < 0) {
        resultado = 0;
    }
    $("#id_punto_equilibrio").val(Math.ceil(resultado));
});

$(".egreso-fijo").change(function (e) {
    var total1 = CalcularEgresos('egreso-fijo');
    var total2 = CalcularEgresos('egreso-variable');
    var total = total1 + total2;
    var ingreso = unformatNumber($('#id_ingreso_neto_total').val());
    var utilidad = ingreso - total;

    if (isNaN(utilidad) || !isFinite(utilidad))
        utilidad = 0.00

    var margen = utilidad / ingreso * 100;

    if (isNaN(margen) || !isFinite(margen))
        margen = 0.00

    $("#id_total_egresos_fijos").val(formatNumber(total1));
    $("#id_total_egresos").val(formatNumber(total)).trigger('change');
    $("#resumen_egreso").val(formatNumber(total));
    $("#resumen_egreso_fijo").val(formatNumber(total1));
    $('#id_utilidad').val(formatNumber(utilidad));

    if (+utilidad < 0) {
        $('#id_utilidad').addClass('border border-danger red-text');
    }
    else {
        $('#id_utilidad').removeClass('border border-danger red-text');
    }

    $("#id_margen_contribucion").val(margen.toFixed(2))
    if (+margen < 0) {
        $('#id_margen_contribucion').addClass('border border-danger red-text');
    }
    else {
        $('#id_margen_contribucion').removeClass('border border-danger red-text');
    }
});

$(".egreso-variable").change(function (e) {
    var total1 = CalcularEgresos('egreso-variable');
    var total2 = CalcularEgresos('egreso-fijo');
    var total = total1 + total2;
    var ingreso = unformatNumber($('#id_ingreso_neto_total').val());
    var utilidad = ingreso - total;
    var margen = utilidad / ingreso * 100;

    $("#id_total_egresos_variables").val(formatNumber(total1));
    $("#id_total_egresos").val(formatNumber(total)).trigger('change');
    $("#resumen_egreso").val(formatNumber(total));
    $("#resumen_egreso_variable").val(formatNumber(total1));
    $('#id_utilidad').val(formatNumber(utilidad));
    $("#id_margen_contribucion").val(isNaN(margen) ? null : formatNumber(margen));
    var resultado2 = total1 / +$("#id_n_participantes").val();
    $('#id_egreso_variable_unit').val(isNaN(resultado2) ? null : formatNumber(resultado2)).trigger('change');

    if (+utilidad < 0) {
        $('#id_utilidad').addClass('border border-danger red-text');
    }
    else {
        $('#id_utilidad').removeClass('border border-danger red-text');
    }

    $("#id_margen_contribucion").val(isNaN(margen) ? null : margen.toFixed(2))
    if (+margen < 0) {
        $('#id_margen_contribucion').addClass('border border-danger red-text');
    }
    else {
        $('#id_margen_contribucion').removeClass('border border-danger red-text');
    }
});


$('.impuesto-select').change(function (event) {
    var valor = (unformatNumber($("#" + event.target.dataset.depend).val()) / 100);
    if ($(this).prop('checked')) {
        $("#" + event.target.dataset.field).val(valor);
        if ($("#id_estado").val() === "Grabado")
            $("#" + event.target.dataset.depend).attr("readonly", false);
    }
    else {
        $("#" + event.target.dataset.field).val(0);
        $("#" + event.target.dataset.depend).attr("readonly", true).val(0);
    }
    $("#" + event.target.dataset.label).trigger('change');
    CalcularHonorarios();
});

$('.porcentaje-impuesto').change(function (event) {
    $('.impuesto-select').trigger('change');
})

$(".total-honorario").change(function (e) {
    var total = +$(this).val();
    var ingresos = unformatNumber($('#id_ingreso_neto_total').val());
    var resultado = total / +ingresos * 100;
    if (isNaN(resultado) || !isFinite(resultado)) {
        $('#' + e.target.dataset.porc).val(0);
    }
    else {
        $('#' + e.target.dataset.porc).val(resultado.toFixed(0));
        if (resultado > 20 && resultado <= 100) {
            alert("Los honorarios superan el 20% del ingreso neto del evento.")
        }
    }
});

$('#id_hospedaje_alimentacion_personal_total').change(function (e) {
    if (+$(this).val() > 96) {
        alert("Máximo 96 diarios si pernota fuera de la ciudad");
    }
})

$('#id_movilizacion_personal_total').change(function (e) {
    if (+$(this).val() > 96) {
        alert("Máximo 96 diarios si pernota fuera de la ciudad");
    }
})

$(document).on('click', "#pnuevo", function () {
    $('#id_ruc_ci').select2('close');
    $('#id_razon_nombres').select2('close');
})

$(document).on('change', '#id_tipo', function (e) {
    load_data($(this).val() == "Jurídica" ? 0 : 1);
});

$(document).on('change', '#id_razon_nombres', function () {
    if ($(this).val() != "") {
        var valor = $('#id_ruc_ci' + " option[name='" + $(this).val() + "']").val();
        $('#id_ruc_ci').val(valor).trigger('change.select2');
    }
    else {
        $('#id_ruc_ci').val(null).trigger('change.select2');
    }
    $('#id_razon_nombres').select2('close');
});

$(document).on('change', '#id_ruc_ci', function () {
    if ($(this).val() != "") {
        var valor = $('#id_razon_nombres' + " option[name='" + $(this).val() + "']").val();
        $('#id_razon_nombres').val(valor).trigger('change.select2');
    }
    else {
        $('#id_razon_nombres').val(null).trigger('change.select2');
    }
    $('#id_ruc_ci').select2('close');
});

$(document).on('click', "#div_id_ruc_ci span.selection", function (e) {
    load_data();
});

$(document).on('click', "#div_id_razon_nombres span.selection", function (e) {
    load_data();
});


$(document).on('change', '#nombre_evento', function () {
    autocomplete($(this), 'codigo_evento');
    CambiarEstado();
    GG();
});

$(document).on('change', '#codigo_evento', function () {
    autocomplete($(this), 'nombre_evento');
    CambiarEstado();
    GG();
    
});

function GG(){
    $("#id_evento").val($('#codigo_evento').val());
    $("#modalidad_evento").val($('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-modalidad"));
    $("#resumen_nombre_evento").val($('#nombre_evento option[value="' + $('#id_evento').val() + '"]').text());
    $('#nombre_evento option[value="' + $('#id_evento').val() + '"]').val()
    var finicio = $('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-finicio");
    var ffin = $('#nombre_evento option[value="' + $('#id_evento').val() + '"]').attr("data-ffin");
    if(finicio==undefined || ffin==undefined){
        $("#fecha_inicio_evento").val(null);
        $("#fecha_fin_evento").val(null);
        return;
    }
    var ymd = finicio.split("/");
    $("#fecha_inicio_evento").val(ymd[2] + "-" + ymd[1] + "-" + ymd[0]);
    var ymd = ffin.split("/");
    $("#fecha_fin_evento").val(ymd[2] + "-" + ymd[1] + "-" + ymd[0]);
}