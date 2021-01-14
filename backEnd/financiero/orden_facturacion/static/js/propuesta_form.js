var p_url = "";
var sector="";

// $('.select3').select2({
//   minimumInputLength: 2,
//   language: {

//     noResults: function () {
//       $(".select2-results__options").append("<a id='pnuevo' class='btn btn-secondary btn-block btn-sm' href='" + p_url + "' target='_blank'>Agregar Nuevo</a>");
//       return "No hay resultados";
//     },
//     searching: function () {

//       return "Buscando...";
//     },
//     inputTooShort: function (e) {
//       var t = e.minimum - e.input.length;
//       return "Ingresa " + t + " caractéres para buscar";
//     }
//   }
// });

// $("#field-ruc-ci [data-select2-id=3]").remove();
// $("#field-ruc-ci [data-select2-id=4]").remove();
// $("#field-razon [data-select2-id=4]").remove();
// $("#field-razon [data-select2-id=5]").remove();
$("#id_ruc_ci").prop('disabled', true);
$("#id_razon_nombres").prop('disabled', true);


$(document).on('change', "#select2-id_reporte-container", function (e) {
  console.log("se hizo");
  var reporte=$("#select2-id_reporte-container").attr("title");
  console.log(reporte);
  var datos=reporte.split(" ");
  const ruc=datos[1];
  console.log(ruc);
 /* $('#id_ruc_ci  option').filter(function() { 
    return ($(this).text() == ruc); //To select Blue
  }).prop('selected', true);*/
  
  
  const razon=$('#id_ruc_ci option').filter(function() { 
    return ($(this).val() == ruc); //To select Blue
  }).attr("name");
  $('#rc').val(ruc);
  $('#rn').val(razon);
  /*$('#id_ruc_ci').val(ruc);
  $('#id_razon_nombres').val(razon);
  $('#id_ruc_ci').trigger('change.select2');
  $('#id_razon_nombres').trigger('change.select2');*/
  load_data();
  load_info();
  
});


function load_info() {
  var url = $('#form-fact').attr("data-info-url");
  var per="";
  var id=0;
  if(flag){
    var id= $('#id_ruc_ci').val();
    if(id==null){
      id=$('#rc').val();
    }
    per="Jurídica";
    console.log(1)
  }
  else{
    var id= $('#rc').val();
    per="Jurídica";
    console.log(2)
  }
  console.log($('#rc').val());
  console.log(flag)
  console.log(id);
  console.log(per);
  $.ajax({
    url: url,
    data: {
      'id': id,
      'persona': "Jurídica",
    },
    success: function (data) {
      flag=false;
      console.log(data.sector)
    
      $('#id_sector option').filter(function() { 
            return ($(this).text() == data.sector); //To select Blue
        }).prop('selected', true);
      $('#id_tipo_empresa option').filter(function() { 
            return ($(this).text() == data.tipo); //To select Blue
        }).prop('selected', true);
      $("#contacto").val(data.contacto);
      $("#telefono").val(data.telefono);
      $("#direccion").val(data.direccion);
    }
  })
}



function load_data() {
  var url = $('#form-fact').attr("data-persona-url");
  var persona = "Jurídica";

  if (persona != "") {
    $.ajax({
      url: url,
      data: {
        'persona': persona
      },
      success: function (data) {
        $("#id_ruc_ci").html(data.ruc_ci)
        $("#id_razon_nombres").html(data.razon_nombre)
        $('#id_ruc_ci').val($('#rc').val());
        $('#id_razon_nombres').val($('#rn').val());
        $('#id_ruc_ci').trigger('change.select2')
        $('#id_razon_nombres').trigger('change.select2')
        //$('#select2-id_ruc_ci-container').text($('#rc').val());
        //$('#select2-id_razon_nombres-container').text($('#rn').val());
      }
    });
    $('#field-razon').show();
    $('#field-ruc-ci').show();

    if (persona == "Natural") {
      $('#ruc_ci').text('CI');
      $('#ra_nom').text('Nombre');
      p_url = $('#form-fact').attr("data-natural-url");
    }
    else if (persona == "Jurídica") {
      $('#ruc_ci').text('RUC');
      $('#ra_nom').text('Razón Social');
      p_url = $('#form-fact').attr("data-juridica-url");
    }
    $("#contacto").val("");
    $("#telefono").val("");
    $("#direccion").val("");
  }
  else {
    $('#field-razon').hide();
    $('#field-ruc-ci').hide();
  }
};

//Autocompleta de un select a otro usando el id
function autocomplete(from, to) {
  if (from.val() != "") {
    $('#' + to).val($('#' + to + " option[name='" + from.val() + "']").val());
    $('#select2-' + to + '-container').text($('#' + to).val());
  }
  else {
    $('#' + to).val("");
    $('#select2-' + to + '-container').text("---------");
  }
  load_info();
  $("#rc").val($("#id_ruc_ci").val());
  $("#rn").val($("#id_razon_nombres").val());
}



$(document).ready(function () {
  flag=true;
  load_data();
  load_info();
});


$(document).on('change', '#id_tipo_cliente', load_data)

$(document).on('change', '#id_razon_nombres', function () {
  autocomplete($(this), 'id_ruc_ci');
});

$(document).on('change', '#id_ruc_ci', function () {
  autocomplete($(this), 'id_razon_nombres');
});


/*
$(document).on('change', '.select2-participantes', function () {
  var clickedselect = $(this).val();
  var id = $(this).attr('id');
  $('.select2-participantes').each(function (e) {
    if ($(this).attr('id') != id) {
      if ($(this).val() == clickedselect) {
        $(this).val("None").trigger('change');
      }
    }
  });
});*/

/*var forma = $("#form-fact");
forma.click(function (e) {
  e.preventDefault();*/
$("#confirmar_guardar").click(function (e) {
  $.ajax({
    url: $('#form-fact').attr("data-confirmacion-url"),
    success: function (data) {
      $('.modal-body').html(data);
    },
  });
})

$(document).on('click', "#pnuevo", function () {
  $('#id_ruc_ci').select2('close');
  $('#id_razon_nombres').select2('close');
})

$(document).on('click', "#div_id_ruc_ci span.selection", function (e) {
  console.log($("#id_ruc_ci").attr("disabled"))
  const dis=$("#id_ruc_ci").attr("disabled");
  if(dis!="disabled"){
    $("#rc").val("");
    $("#rn").val("");
    load_data();
  }
});

$(document).on('click', "#div_id_razon_nombres span.selection", function (e) {
  const dis=$("#id_razon_nombres").attr("disabled");
  if(dis!="disabled"){
    $("#rc").val("");
    $("#rn").val("");
    load_data();
  }
});

$(document).on('click', "#hack", function (e) {
  $("#id_version").prop('disabled', false);
  $("#id_ruc_ci").prop('disabled', false);
  $("#id_razon_nombres").prop('disabled', false);

  const valmp=$("#id_monto_propuesta").val();
  $("#id_monto_propuesta").attr("type","number");
  $("#id_monto_propuesta").val(parseFloat(valmp.replace(/,/g,"")));
  $("#id_monto_propuesta").val(parseFloat($("#id_monto_propuesta").val()).toFixed(2));

  const value=$("#id_utilidad_esperada").val();
  $("#id_utilidad_esperada").attr("type","number");
  $("#id_utilidad_esperada").val(parseFloat(value.replace(/,/g,"")));
  $("#id_utilidad_esperada").val(parseFloat($("#id_utilidad_esperada").val()).toFixed(2));
  
});

$(document).on('click', "#hack2", function (e) {
  $("#id_version").prop('disabled', false);
  $("#id_ruc_ci").prop('disabled', false);
  $("#id_razon_nombres").prop('disabled', false);

  const valmp=$("#id_monto_propuesta").val();
  $("#id_monto_propuesta").attr("type","number");
  $("#id_monto_propuesta").val(parseFloat(valmp.replace(/,/g,"")));
  $("#id_monto_propuesta").val(parseFloat($("#id_monto_propuesta").val()).toFixed(2));

  const value=$("#id_utilidad_esperada").val();
  $("#id_utilidad_esperada").attr("type","number");
  $("#id_utilidad_esperada").val(parseFloat(value.replace(/,/g,"")));
  $("#id_utilidad_esperada").val(parseFloat($("#id_utilidad_esperada").val()).toFixed(2));
  
});

//Evento para quitar el fondo azul al hacer el autocomplete de los text inputs
/*$(document).on('change', "input", function (e) {
  if ($(this).attr("type")!="checkbox"){
    $(this).css("box-shadow", "0 0 0px 1000px white inset");
}
});*/

// $("#div_id_razon_nombres span").each(function(){
//   const ca=$(this).attr("class")
//   $(this).attr("class",ca+" col-md-10")
// });


// $("#div_id_ruc_ci select + span").each(function(){
//   const ca=$(this).attr("class")
//   $(this).attr("class",ca+" col-md-10")
// });

// $("#div_id_ruc_ci span[class='select2-selection select2-selection--single']").each(function(){
//   const ca=$(this).attr("class")
//   $(this).attr("class",ca+" col-12 col-md-9")
// });

// $("#div_id_razon_nombres span[class='select2-selection select2-selection--single']").each(function(){
//   const ca=$(this).attr("class")
//   $(this).attr("class",ca+" col-md-9")
// });

//para eliminar el modal cuando sea editar
if($("[name=cod_propuesta]").val()!=""){
  console.log("momazo")
  
  var newbutton=$("<button>");
  newbutton.attr("id","hack2");
  newbutton.attr("class","btn btn-secondary green-bg mr-1");
  newbutton.attr("type","submit");
  newbutton.html("Guardar");
  var newcancel=$("<a>");
  newcancel.attr("class","btn btn-secondary");
  newcancel.html("Cancelar");
  var remp=$("#remplazo");
  var remp2=$("#remplazo2").remove();
  var parent=remp.parent();
  newcancel.attr("href",remp2.attr("href"));
  remp.remove();
  remp2.remove();
  parent.append(newbutton);
  parent.append(newcancel);

}