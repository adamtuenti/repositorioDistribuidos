
function back(input){
    const val=$(input).val();
    const val2=val.replace("$","").replace(/,/g,"");
    $(input).val(parseFloat(val2));

}

$(document).on('click', '#enviar', function () {
    //cambio de formato
    const Ej=$(".ejec");
    
    Ej.each(function(){
        back(this);
    });

    const Plan=$(".plan");
    Plan.each(function(){
        back(this);
    });

    back($("#id_total_ingresos"));
    back($("#id_total_ingresos_ejec"));
    back($("#id_total_gastos"));
    back($("#id_total_gastos_ejec"));

    //seteo valor del centro
    $("#id_centro_costos").val($("#tipoP").val());
    $("#id_version").prop("disabled",false);
});

