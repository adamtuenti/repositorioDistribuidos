
$("#id_fecha_seguimiento_0").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_seguimiento_0").val()!=""){
    const vars= $("#id_fecha_seguimiento_0").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_seguimiento_0").val(fechan);
        $("#id_fecha_seguimiento_0").attr("type","date");
        
        
    }
    
}

$("#id_fecha_seguimiento_0").attr("placeholder","Fecha Seguimiento Inicial")
$("#id_fecha_seguimiento_1").attr("placeholder","Fecha Seguimiento Final")

$("#id_fecha_seguimiento_1").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_seguimiento_1").val()!=""){
    const vars= $("#id_fecha_seguimiento_1").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_seguimiento_1").val(fechan);
        $("#id_fecha_seguimiento_1").attr("type","date");
        
        
    }
    
}

var fechas = $("input[name*='fecha_seguimiento']");
div_padre_fechas = $(fechas).parent();
div_padre_todo = $(div_padre_fechas).parent();

var div_1 = $("<div class = 'col-4'></div>");
var div_2 = $("<div class = 'col-4'></div>");
$(div_1).append(fechas[0]);
$(div_2).append(fechas[1]);
div_padre_fechas.remove();
div_padre_todo.append(div_1);
div_padre_todo.append(div_2);


$("#id_fecha_registro_1").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_registro_1").val()!=""){
    const vars= $("#id_fecha_registro_1").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_registro_1").val(fechan);
        $("#id_fecha_registro_1").attr("type","date");
        
        
    }
    
}

$("#id_fecha_registro_0").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_registro_0").val()!=""){
    const vars= $("#id_fecha_registro_0").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_registro_0").val(fechan);
        $("#id_fecha_registro_0").attr("type","date");
        
        
    }
    
}

var fechas2 = $("input[name*='fecha_registro']");
div_padre_fechas2 = $(fechas2).parent();
div_padre_todo2 = $(div_padre_fechas2).parent();

var div_12 = $("<div class = 'col-4'></div>");
var div_22 = $("<div class = 'col-4'></div>");
$(div_12).append(fechas2[0]);
$(div_22).append(fechas2[1]);
div_padre_fechas2.remove();
div_padre_todo2.append(div_12);
div_padre_todo2.append(div_22);

$("#id_fecha_registro_0").attr("placeholder","Fecha Registro Inicial")
$("#id_fecha_registro_1").attr("placeholder","Fecha Registro Final")