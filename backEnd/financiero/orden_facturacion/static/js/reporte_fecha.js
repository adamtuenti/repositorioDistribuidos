$("#id_fecha").focusout(function () {
    if($(this).val()==""){
        $(this).attr("type","text");
    }
  })
  
if($("#id_fecha").val()!=""){
    const vars= $("#id_fecha").val();
    const listv=vars.split("-");
    if(listv.length>1){
        const fechan=listv[0]+"-"+listv[1]+"-"+listv[2];
        $("#id_fecha").val(fechan);
        $("#id_fecha").attr("type","date");
        
    }
    
}