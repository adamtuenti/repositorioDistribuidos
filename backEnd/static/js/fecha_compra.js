$("#id_fecha_facturacion_0").focusout(function() {
    if ($(this).val() == "") {
        $(this).attr("type", "text");
    }
})

if ($("#id_fecha_facturacion_0").val() != "") {
    const vars = $("#id_fecha_facturacion_0").val();
    const listv = vars.split("-");
    if (listv.length > 1) {
        const fechan = listv[0] + "-" + listv[1] + "-" + listv[2];
        $("#id_fecha_facturacion_0").val(fechan);
        $("#id_fecha_facturacion_0").attr("type", "date");
    }
}

$("#id_fecha_facturacion_0").attr("placeholder", "Fecha inicio")
$("#id_fecha_facturacion_1").attr("placeholder", "Fecha fin")

$("#id_fecha_facturacion_1").focusout(function() {
    if ($(this).val() == "") {
        $(this).attr("type", "text");
    }
})

if ($("#id_fecha_facturacion_1").val() != "") {
    const vars = $("#id_fecha_facturacion_1").val();
    const listv = vars.split("-");
    if (listv.length > 1) {
        const fechan = listv[0] + "-" + listv[1] + "-" + listv[2];
        $("#id_fecha_facturacion_1").val(fechan);
        $("#id_fecha_facturacion_1").attr("type", "date");
    }
}

var fechas = $("input[name*='fecha_facturacion']");
div_padre_fechas = $(fechas).parent();
div_padre_todo = $(div_padre_fechas).parent();

var div_1 = $("<div class = 'col-3'></div>");
var div_2 = $("<div class = 'col-3'></div>");
$(div_1).append(fechas[0]);
$(div_2).append(fechas[1]);
div_padre_fechas.remove();
div_padre_todo.append(div_1);
div_padre_todo.append(div_2);