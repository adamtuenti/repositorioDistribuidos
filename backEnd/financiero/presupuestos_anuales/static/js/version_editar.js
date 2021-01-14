$("#id_version").attr("type","number");
const valV=$("#id_version").val();


$("#id_version").change(function(){
    const valN=$(this).val();

    if(parseInt(valN)<parseInt(valV)){
        $(this).val(valV);
    }else if(parseInt(valN)>(parseInt(valV)+1)){
        $(this).val(parseInt(valV)+1);
    }

});


if($("#id_active").val()=="False"){
    $("#id_version").prop("disabled",true);
}