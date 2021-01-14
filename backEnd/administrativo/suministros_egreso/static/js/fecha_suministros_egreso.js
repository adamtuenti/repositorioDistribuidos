
$("#id_fecha_egreso_0").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_egreso_0").val()!=""){
    const vars= $("#id_fecha_egreso_0").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_egreso_0").val(fechan);
        $("#id_fecha_egreso_0").attr("type","date");
        
        
    }
    
}

$("#id_fecha_egreso_0").attr("placeholder","Fecha inicio")
$("#id_fecha_egreso_1").attr("placeholder","Fecha fin")

$("#id_fecha_egreso_1").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha_egreso_1").val()!=""){
    const vars= $("#id_fecha_egreso_1").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha_egreso_1").val(fechan);
        $("#id_fecha_egreso_1").attr("type","date");
        
        
    }
    
}

var fechas = $("input[name*='fecha_egreso']");
div_padre_fechas = $(fechas).parent();
div_padre_todo = $(div_padre_fechas).parent();

var div_1 = $("<div class = 'col-4'></div>");
var div_2 = $("<div class = 'col-4'></div>");
$(div_1).append(fechas[0]);
$(div_2).append(fechas[1]);
div_padre_fechas.remove();
div_padre_todo.append(div_1);
div_padre_todo.append(div_2);

// $(document).ready(function () {
//     var fechas = $("input[name*='fecha_egreso']");
//     div_padre_fechas = $(fechas).parent();
//     div_padre_todo = $(div_padre_fechas).parent();
//     console.log(div_padre_fechas);
//     console.log(div_padre_todo);

//     console.log(fechas[0]);
//     $(fechas[0]).attr({"placeholder":"Fecha inicio"});
//     $(fechas[1]).attr({"placeholder":"Fecha fin"});
//     console.log(fechas[1]);
//     $(fechas[0]).focus(function(e){
//         $(this).attr("type","date");
//     });
//     $(fechas[1]).focus(function(e){
//         $(this).attr("type","date");
//     });    
//     $(fechas[0]).focusout(function(e){
//         if($(this).val()==""){
//             $(this).attr("type","text");
//         }

//     });
//     $(fechas[1]).focusout(function(e){
//         if($(this).val()==""){
//             $(this).attr("type","text");
//         }

//     });
//     if($(fechas[0]).val()!=""){
//         console.log("no esta vacio");
//         const vars= $(fechas[0]).val();
//         const listv=vars.split("-");
//         if(listv.length>1){
//             const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
//             $(this).val(fechas[0]);
//             $(this).attr("type","date");
            
//         }
//     }
//     if($(fechas[1]).val()!=""){
//         console.log("no esta vacio");
//         const vars= $(fechas[0]).val();
//         const listv=vars.split("-");
//         if(listv.length>1){
//             const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
//             $(this).val(fechas[0]);
//             $(this).attr("type","date");
            
//         }
//     }
   
//     var div_1 = $("<div class = 'col-4'></div>");
//     var div_2 = $("<div class = 'col-4'></div>");
//     $(div_1).append(fechas[0]);
//     $(div_2).append(fechas[1]);
//     div_padre_fechas.remove();
//     div_padre_todo.append(div_1);
//     div_padre_todo.append(div_2);
   
// });
