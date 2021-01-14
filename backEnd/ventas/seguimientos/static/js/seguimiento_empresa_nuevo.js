function init_select2() {
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
}

function load_eventos(tipo) {
    var url = $('#form-seg').attr("data-evento-url");
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
    var url = $('#form-seg').attr("data-reporte-url");
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
    var url = $('#form-seg').attr("data-participante-url");
    if (cod === "") {
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

function load_oferta(tipo_oferta, juridica) {
    var url = $('#form-seg').attr("data-oferta-url");
    $.ajax({
        url: url,
        data: {
            "tipo": tipo_oferta,
            "ruc": juridica
        },
        success: function (data) {
            $("#id_n_oferta").html(data);
            $("#id_n_oferta").val($("#n_oferta").val()).trigger('change.select2');
        }
    })
}


var n_form = 0;

function SetNum(value) {
    n_form = 1;
    for (let index = 1; index < +(value); index++) {
        AddForm(index);
        n_form++;
    }
}

$(document).on('click', '#add-evento', function (e) {
    e.preventDefault();
    if ($(".formset:not('.d-none'):last select").val() != "") {
        AddForm(n_form);
        n_form++;
    }
});

function init_all() {
    init_select2();
    $(".formset .evento").each(function (index, val) {
        var parent = $(this);
        var hidden = parent.find("input:hidden:first");
        var select_cod = parent.find("select:first");
        var select_nom = parent.find("select:last");
        select_cod.change(function (e) {
            AssignVerify($(this), select_nom, hidden);
        })
        select_nom.change(function (e) {
            AssignVerify($(this), select_cod, hidden);
        })
    })
    var n_participantes = $("#id_n_participantes").val();
    $("#id_tipo_oferta").trigger('change');
    $("#id_n_participantes").val(n_participantes);
    load_reportes($('#id_juridica').val());
    SetNum($("#id_n_evento").val())
}


function AssignVerify(select1, select2, hidden) {
    var val = select1;
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

function countFullForms() {
    var n = 0;
    $(".formset:not('.d-none')").find("select:first").each(function (e) {
        n += $(this).val() !== "" ? 1 : 0;
    })
    return n;
}

function AddForm(index) {
    $('.formset').eq(index).removeClass('d-none');
}

function RemoveForm(index) {
    $('.formset').eq(index).addClass('d-none');
}


$(document).on('change', '#id_tipo_oferta', function (e) {
    if ($(this).val() === "Directa" || $(this).val() === '') {
        $("#n_oferta").val(null);
        $("#id_n_oferta").attr('disabled', true).val(null).trigger('change.select2');
        $("#id_n_participantes").attr('readonly', false);
        if ($("#id_tipo_evento").val() === "Corporativo") {
            $("#id_estado").attr('disabled', true).val(3);
        }
    }
    else {
        load_oferta($(this).val(), $("#id_juridica").val());
        $("#id_n_oferta").attr('disabled', false).val(null).trigger('change.select2');;
        $("#id_n_participantes").attr('readonly', true).val(null);
        $("#id_estado").attr('disabled', false);
    }
});

$(document).on('change', '#id_tipo_evento', function (e) {
    if ($(this).val() === "Corporativo" && $("#id_tipo_oferta").val() === "Directa") {
        $("#id_estado").attr('disabled', true).val(3);
    }
    else {
        $("#id_estado").attr('disabled', false);
    }
});


$(document).on('change', '#razon', function (e) {
    autocomplete($(this), 'ruc');
    $("#id_juridica").val($('#ruc').val());
    load_reportes($('#ruc').val());
})

$(document).on('change', '#ruc', function (e) {
    autocomplete($(this), 'razon');
    $("#id_juridica").val($('#ruc').val());
    load_reportes($('#ruc').val());
})

$(document).on('change', '#id_n_oferta', function (e) {
    $("#n_oferta").val($(this).val());
    load_participante($(this).val(), $("#id_tipo_oferta").val())
})

$(document).on('click', '#enviar', function (e) {
    e.preventDefault();
    $("#id_estado").attr('disabled', false);
    $("#id_n_evento").val(countFullForms());
    $('#form-seg').trigger('submit');
});

$(document).on('submit', "#form-seg", function (e) {
    // Stop form from submitting normally
    e.preventDefault();
    var myform = $(this);
    var url = myform.attr("data-post-url");
    $.ajax({
        type: 'POST',
        url: url,
        data: myform.serialize(),
        dataType: 'json',
        success: function (response) {
            myform.trigger('reset')
            $("#personaModal").modal('hide');
            var content = $("<div>");
            var span = $("<span>");
            span.html(response.msj);
            content.append(span);
            $("#respuesta-post .modal-body").html(content);
            $("#respuesta-post").modal('show');
        },
        error: function (response) {
            $("#personaModal .modal-content").html(response["responseText"])
            init_all();
        }
    });
})

$(document).on('change', "#id_tipo_evento", function (e) {
    load_eventos($(this).val());
})

/**
 * Function to setup an ajax post. Useful to display form with errors when the server responses
 */
$(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});