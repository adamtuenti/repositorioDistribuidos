$('.select2').select2({
    width: '100%',
    language: {

        noResults: function () {
            return "No hay resultados";
        },
        searching: function () {

            return "Buscando...";
        },
    }
});

function autocomplete(from, to) {
    if (from.val() != "") {
        $('#' + to).val($('#' + to + " option[name='" + from.val() + "']").val());
        $('#' + to).trigger('change.select2');
    }
    else {
        $('#' + to).val(null).trigger('change.select2');
    }
}

function load_eventos(tipo) {
    var url = $('form').attr("data-evento-url");
    $.ajax({
        url: url,
        data: {
            'tipo': tipo
        },
        success: function (data) {
            $('select[id$="codigo_evento"]').html(data.codigo);
            $('select[id$="nombre_evento"]').html(data.nombre);
        }
    });
}

function load_reportes(ruc) {
    var url = $('form').attr("data-reporte-url");
    $.ajax({
        url: url,
        data: {
            'id': ruc
        },
        success: function (data) {
            $('#id_reporte_contacto').html(data);
            $('#id_reporte_contacto').val($("#reporte_contacto").val());
        }
    });
}

function load_participante(cod, oferta) {
    var url = $('form').attr("data-participante-url");
    if (cod==="") {
        $("#id_n_participantes").val(null)
        return;
    }
    $.ajax({
        url: url,
        data: {
            'oferta': oferta,
            'cod': cod
        },
        success: function (data) {
            $("#id_n_participantes").val(data)
        }
    });
}

function load_oferta(tipo_oferta,juridica){
    var url = $('form').attr("data-oferta-url");
    $.ajax({
        url:url,
        data:{
            "tipo":tipo_oferta,
            "ruc":juridica
        },
        success: function(data){
            $("#id_n_oferta").html(data);
            $("#id_n_oferta").val($("#n_oferta").val()).trigger('change.select2');
        }
    })
}


var n_form=0;

function SetNum(value) {
    n_form = 1;
    for (let index = 1; index < +(value); index++) {
        AddForm(index);
        n_form ++;
    }
}

$("#add-evento").click(function (e) {
    e.preventDefault();
    if ($(".formset:not('.d-none'):last select").val() != "") {
        AddForm(n_form);
        n_form++;
    }
});

$(".formset .evento").each(function (index, val) {
    var parent = $(this);
    var hidden = parent.find("input:hidden:first");
    var select_cod = parent.find("select:first");
    var select_nom = parent.find("select:last");
    select_cod.change(function (e) {
        AssignVerify($(this),select_nom, hidden);
    })
    select_nom.change(function (e) {
        AssignVerify($(this),select_cod, hidden);
    })
})

function AssignVerify(select1,select2, hidden) {
    var val =select1;
    if (val.val() !== "") {
        var igual = false;
        $(".formset:not('.d-none')").find("select:first").each(function (e) {
            if ($(this).attr('id') !== val.attr('id')) {
                if ($(this).val() === val.val()) {
                    val.val(null).trigger('change.select2');
                    igual = true;
                    return false;
                }
            }
        });

    }
    select2.val(val.val()).trigger('change.select2');
    hidden.val(val.val());
}

function countFullForms(){
    var n=0;
    $(".formset:not('.d-none')").find("select:first").each(function (e) {
        n += $(this).val()!=="" ? 1:0;
    })
    return n;
}

function AddForm(index) {
    $('.formset').eq(index).removeClass('d-none');
}

function RemoveForm(index) {
    $('.formset').eq(index).addClass('d-none');
}

$("#id_tipo_oferta").change(function (e) {
    if ($(this).val() === "Directa" || $(this).val() === '') {
        $("#n_oferta").val(null);
        $("#id_n_oferta").attr('disabled', true).val(null).trigger('change.select2');;
        $("#id_n_participantes").attr('readonly', false);
        if($("#id_tipo_evento").val()==="Corporativo"){
            $("#id_estado").attr('disabled', true).val(3);
        }
    }
    else {
        load_oferta($(this).val(),$("#id_juridica").val());
        $("#id_n_oferta").attr('disabled', false).val(null).trigger('change.select2');;
        $("#id_n_participantes").attr('readonly', true).val(null);
        $("#id_estado").attr('disabled', false);
    }
});

$("#id_tipo_evento").change(function (e) {
    if ($(this).val() === "Corporativo" && $("#id_tipo_oferta").val()==="Directa") {
        $("#id_estado").attr('disabled', true).val(3);
    }
    else {
        $("#id_estado").attr('disabled', false);
    }
});

$('#enviar').click(function (e) {
    e.preventDefault();
    $("#id_estado").attr('disabled', false);
    $("#id_n_evento").val(countFullForms());
    $('form').trigger('submit');
});

$('#razon').on('change', function () {
    autocomplete($(this), 'ruc');
    $("#id_juridica").val($('#ruc').val());
    load_reportes($('#ruc').val());
})

$('#ruc').on('change', function () {
    autocomplete($(this), 'razon');
    $("#id_juridica").val($('#ruc').val());
    load_reportes($('#ruc').val());
})

$('#id_n_oferta').change(function () {
    $("#n_oferta").val($(this).val());
    load_participante($(this).val(), $("#id_tipo_oferta").val())
})

$(document).on('change', "#id_tipo_evento", function (e) {
    load_eventos($(this).val());
})

$(document).ready(function (e) {
    var n_participantes=$("#id_n_participantes").val();
    $("#id_tipo_oferta").trigger('change');
    $("#id_n_participantes").val(n_participantes);
    load_reportes($('#id_juridica').val());
})