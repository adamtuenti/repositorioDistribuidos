$(document).on('change', '#id_participante_cedula', function () {
  autocomplete($(this), 'id_participante_nombre');
  if($("#id_participante_cedula").val()==""){
    $("#codigoO").prop("disabled",true);
    $("#nombreEO").prop("disabled",true);
    $("#codigoD").prop("disabled",true);
    $("#nombreED").prop("disabled",true);
    limpiar();
  }else{
    load_participante_evento();
    load_participanteNo_evento();
    $("#codigoO").prop("disabled",false);
    $("#nombreEO").prop("disabled",false);
    $("#codigoD").prop("disabled",false);
    $("#nombreED").prop("disabled",false);

    $("#EventoDestinoTablaBody").find("tr").each(function(){
      $(this).find(".eliminarEventoDinamico").trigger("click");
      $(this).html("");
    });

  }
});

$(document).on('change', '#id_participante_nombre', function () {
  autocomplete($(this), 'id_participante_cedula');
  if($("#id_participante_cedula").val()==""){
    $("#codigoO").prop("disabled",true);
    $("#nombreEO").prop("disabled",true);
    $("#codigoD").prop("disabled",true);
    $("#nombreED").prop("disabled",true);
    limpiar();
  }else{
    load_participante_evento();
    load_participanteNo_evento();
    $("#codigoO").prop("disabled",false);
    $("#nombreEO").prop("disabled",false);
    $("#codigoD").prop("disabled",false);
    $("#nombreED").prop("disabled",false);

    $("#EventoDestinoTablaBody").find("tr").each(function(){
      $(this).find(".eliminarEventoDinamico").trigger("click");
      $(this).html("");
    });

  }
});

function limpiar(){
  $("#evento-origen").find("td").each(function(){
    $(this).html("");
  });

  $("#EventoDestinoTablaBody").find("tr").each(function(){
    $(this).find(".eliminarEventoDinamico").trigger("click");
    $(this).html("");
  });

  $("#codigoO").val("").trigger("change");
  $("#nombreEO").val("").trigger("change");
  $("#codigoD").val("").trigger("change");
  $("#nombreED").val("").trigger("change");

}


$(document).on('change', '#codigoO', function () {
  autocomplete($(this), 'nombreEO');
  if($("#codtEO").html()=="" && $("#codigoO").val()!=""){
    datos_eventos2($("#codigoO").val(), "ORIGEN");
  }
  
});

$(document).on('change', '#nombreEO', function () {
  autocomplete($(this), 'codigoO');
  if($("#codtEO").html()=="" && $("#codigoO").val()!=""){
    datos_eventos2($("#codigoO").val(), "ORIGEN");
  }
  
});

$(document).on('change', '#codigoD', function () {
  autocomplete($(this), 'nombreED');
  console.log(verificarExistenciaEvento($("#codigoD").val()))
  if($("#codigoD").val()!="" && verificarExistenciaEvento($("#codigoD").val())){
    datos_eventos2($("#codigoD").val(), "DESTINO");
  }
  
});

$(document).on('change', '#nombreED', function () {
  autocomplete($(this), 'codigoD');
  if($("#codigoD").val()!="" && verificarExistenciaEvento($("#codigoD").val())){
    datos_eventos2($("#codigoD").val(), "DESTINO");
  }
});

$(document).on('click', '#hack2', function () {
    $("#id_evento_origen_codigo").val($("#codtEO").html());
    $("#id_evento_origen_nombre").val($("#nomtEO").html());
    $("#id_evento_origen_valor").val($("#evtEO").html());
  });



$(document).on('click', '.eliminarEvent', function () {
  var row=$(this).parent().parent();
  $(row).children().each(function(){
     $(this).html("");
  });
});

$(document).on('click', '.eliminarEventoDinamico', function () {
  var row=$(this).parent().parent();
  var children=row.children();
  var cod=$(children[0]).html();
  console.log(cod)
  deleteForm('form', cod);
  row.remove();
});