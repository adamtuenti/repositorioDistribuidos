

$("#id_fechaSolicitud").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fechaSolicitud").val()!=""){
    const vars= $("#id_fechaSolicitud").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fechaSolicitud").val(fechan);
        $("#id_fechaSolicitud").attr("type","date");
        
    }
    
}

$("#id_fechaEnvio").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fechaEnvio").val()!=""){
    const vars= $("#id_fechaEnvio").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fechaEnvio").val(fechan);
        $("#id_fechaEnvio").attr("type","date");
        
    }
    
}