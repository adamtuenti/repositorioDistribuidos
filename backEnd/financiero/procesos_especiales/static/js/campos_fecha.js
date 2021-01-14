


$("#id_fechas_emision_0").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fechas_emision_0").val()!=""){
    const vars= $("#id_fechas_emision_0").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fechas_emision_0").val(fechan);
        $("#id_fechas_emision_0").attr("type","date");
        
        
    }
    
}

$("#id_fechas_emision_0").attr("placeholder","Fecha Emisión Inicial")
$("#id_fechas_emision_1").attr("placeholder","Fecha Emisión Final")

$("#id_fechas_emision_1").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fechas_emision_1").val()!=""){
    const vars= $("#id_fechas_emision_1").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fechas_emision_1").val(fechan);
        $("#id_fechas_emision_1").attr("type","date");
        
        
    }
    
}

var fechas = $("input[name*='fechas_emision']");
div_padre_fechas = $(fechas).parent();
div_padre_todo = $(div_padre_fechas).parent();

var div_1 = $("<div class = 'col-2'></div>");
var div_2 = $("<div class = 'col-2'></div>");
$(div_1).append(fechas[0]);
$(div_2).append(fechas[1]);
div_padre_fechas.remove();
div_padre_todo.append(div_1);
div_padre_todo.append(div_2);