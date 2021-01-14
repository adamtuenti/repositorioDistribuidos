$('.select4').select2({
  minimumInputLength: 0,
  width: '100%',
  language: {
    noResults: function () {
      return "No hay resultados";
    },
    searching: function () {

      return "Buscando...";
    }
    ,
    inputTooShort: function (e) {
      var t = e.minimum - e.input.length;
      return "Ingresa " + t + " caractéres para buscar";
    }
  }


});

function load_eventos() {
  var url = $('#form-pe').attr("data-eventos-url");
  var tipo=$("#id_categoria").val();
  if (tipo==""){
    tipo=$("#catLazy").val();
  }
  console.log(tipo)
  $.ajax({
    url: url,
    data: {
      'tipo': tipo,
    },
    success: function (data) {
      $("#codigoEvento").html(data.eventos);
    }
  });

};

function datos_eventos() {
  var cod = $("#codigoEvento").val();
  console.log(cod);
  
  if (cod !== "") {
    var url = $('#form-pe').attr("data-eventosInd-url");
    $.ajax({
      url: url,
      data: {
        'codigo': cod,
      },
      success: function (data) {
        $("#nombreEvento").val(data.evento.nombre);
        $("#id_valor_eventoC").val(transformEdit(data.valor));
        $("#id_descuentoC").val(0);
        $("#id_descuentoC").trigger("change");
      }
    });
  }
  else{
    $("#nombreEvento").val(null);
    $("#id_valor_eventoC").val(null);
    $("#id_descuentoC").val(null);
    $("#id_valor_totalC").val(null);
  }
}

load_eventos();

$(document).on('change', '#codigoEvento', function () {
  datos_eventos();
});



var cat = $("#catLazy").val();
console.log(cat)
if (cat != undefined) {
  console.log("estamos creando")
  $("#id_categoria").val(cat);
  var now = new Date();
  var month = (now.getMonth() + 1);
  var day = now.getDate();
  if (month < 10)
    month = "0" + month;
  if (day < 10)
    day = "0" + day;
  var today = now.getFullYear() + '-' + month + '-' + day;
  $('#id_fecha_emision').val(today);
  if (cat == "Grat") {
    $("#id_tipo_nota").val("Crédito");
  } else {
    $("#id_tipo_nota").val("Débito");
  }
}

console.log($("#id_cod_proceso").val())
if ($("#id_cod_proceso").val() == "") {
  $("#env-sol").remove();
}

$(document).on('click', '#hackTipoNota', function () {
  $("#id_tipo_nota").prop("disabled", false);
  $("#id_categoria").prop("disabled", false);
  $("#id_concepto").prop("disabled", false);

});

$("#id_estado").prop("disabled", true);
$("#id_tipo_nota").prop("disabled", true);
var estado = $("#id_estado").val();
if (estado == "ANLD" || estado == "APRB" || estado == "SOLI") {
  $("#id_categoria").prop("disabled", true);
  $("#id_concepto").prop("disabled", true);
  $("#codigoEvento").prop("disabled", true);
  $("#id_descuentoC").prop("disabled", true);
  $("#add").remove();
  $("#add2").remove();
  $("#env-sol").remove();
  $(".eliminarRow").each(function () {
    $(this).remove();
  });


}
console.log("EL TRUE CAMBIO")
$(document).on('change', '#codigoEvento', function () {
      if($(this).val()!=""){
        if($("#id_categoria").val()=="Part" && $("#tbodyPart").children().length==1 ){
          $("#add").prop("disabled",true);
        }else if(($("#id_categoria").val()=="Event" && $("#id_tipo_nota").val()=="Débito") && $("#tbodyPart").children().length==1 ){
          $("#add").prop("disabled",true);
        }else{
          $("#add").prop("disabled",false);
          
        }
      }else{
        $("#add").prop("disabled",true);
        
      }
});

$("#add").prop("disabled",true);
$("#id_categoria").prop("disabled",true);

$(document).on('change', '#id_descuentoC', function () {
  var desc=$(this).val();
  if(desc<0){
      $(this).val(0);
      desc=0;
  }else if(desc>100){
      $(this).val(100);
      desc=100;
  }
    var valor=$("#id_valor_eventoC").val();
    var num=parseFloat(valor.replace(/,/g,"")).toFixed(2);
    var total=num-(num*desc)/100;
    $("#id_valor_totalC").val(transformEdit(total));
  
});


function transformEdit(numero){
  var num=""+parseFloat(numero).toFixed(2);
  var numeroe=num.split(".")
  const long= numeroe[0].length;
  var newnum="";
  cont=0;
  for(var i=(long-1);i>=0;i--){
        if(cont%3==0 && cont!=0){
          newnum=numeroe[0].charAt(i)+","+newnum;
          cont+=1;
        }else{
          newnum=numeroe[0].charAt(i)+newnum;
          cont+=1;
        }
  }
  return newnum+"."+numeroe[1];
  
}
