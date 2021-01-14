var has_anexo = false;
var has_n_tra = false;
var has_n_fact = false;
var has_f_tra = false;
var has_f_fact = false;
verificar();
function isInteger(str) {
    return /^\d*$/.test(str);
}

function change_state_btn() {
    if (has_anexo && has_n_tra && has_n_fact && has_f_tra && has_f_fact) {
        $("#id_estado").val("PNDP");
    }
    else {
        $("#id_estado").val("ACPF");
    }
}

function verificar() {

    $("#tablefile tr").each(function(){
        var h=$(this).children();
        var a =$(h[0]).find("a");
        console.log($(a).attr("href"));
        if($(a).attr("href")!=undefined){
           has_anexo=true;
        }
    });

    $(".ordenfactf").each(function(){
            if($(this).val()!=""){
                has_anexo=true;
            }

    });
    console.log($("#id_fecha_tramite").val())
    console.log($("#id_fecha_factura").val())

    has_f_tra = $("#id_fecha_tramite").val()!="";

    has_f_fact = $("#id_fecha_factura").val()!="";

    has_n_fact = isInteger($("#id_n_factura").val());

    has_n_tra = isInteger($("#id_n_tramite").val());

    console.log(has_f_tra)
    console.log(has_n_tra)
    console.log(has_anexo)
    console.log(has_f_fact)
    console.log(has_n_fact)

    change_state_btn()
}

$("#id_anexo_factura").change(function () {
    has_anexo = $(this).get(0).files.length !== 0;
    change_state_btn()
});

$("#id_n_factura").focusout(function () {
    has_n_fact = isInteger($(this).val());
    change_state_btn()
});

$("#id_n_tramite").focusout(function () {
    has_n_tra = isInteger($(this).val());
    change_state_btn()
});

$(document).on('click', "#guardar", function (e) {
    verificar();
});