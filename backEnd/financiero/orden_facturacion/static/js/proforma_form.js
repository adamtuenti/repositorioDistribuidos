var p_url = "";

$('.select2').select2({
  minimumInputLength: 2,
  width: '100%',
  language: {

    noResults: function () {
      $(".select2-results__options").append("<a id='pnuevo' class='btn btn-secondary btn-block btn-sm' href='" + p_url + "' target='_blank'>Agregar Nuevo</a>");
      return "No hay resultados";
    },
    searching: function () {

      return "Buscando...";
    },
    inputTooShort: function (e) {
      var t = e.minimum - e.input.length;
      return "Ingresa " + t + " caractéres para buscar";
    }
  }
});


function load_info() {
  var url = $('#form-fact').attr("data-info-url");
  if(flag){
    var id= $('#rc').val();
  }
  else{
    var id= $('#id_ruc_ci').val();
  }
  $.ajax({
    url: url,
    data: {
      'id': id,
      'persona': $("#id_tipo_cliente").val(),
    },
    success: function (data) {
      flag=false;
      $('#id_sector option').filter(function() { 
        return ($(this).text() == data.sector); //To select Blue
    }).prop('selected', true);
  $('#id_tipoEmpresa option').filter(function() { 
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
  var persona = $("#id_tipo_cliente").val();

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
    $('#field-razon').css('visibility', 'visible');
    $('#field-ruc-ci').css('visibility', 'visible');

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
    $('#field-razon').css('visibility', 'hidden');
    $('#field-ruc-ci').css('visibility', 'hidden');
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
  $("#rc").val("");
  $("#rn").val("");
  load_data();
});

$(document).on('click', "#div_id_razon_nombres span.selection", function (e) {
  $("#rc").val("");
  $("#rn").val("");
  load_data();
});


if($("[name=codigo]").val()!=""){
    $(".crear").hide();
    

}else{
  $(".editar").each(function() {
    $(this).hide();
  });

}

//para habilitar la wea de version
$(document).on('click', ".hack", function (e) {
  $("#id_version").prop('disabled', false);

  const val=$("#id_montoProforma").val();
  $("#id_montoProforma").attr("type","number");
  $("#id_montoProforma").val(parseFloat(val.replace(/,/g,"")));
  $("#id_montoProforma").val(parseFloat($("#id_montoProforma").val()).toFixed(2));
  
  const valmd=$("#id_montoDesc").val();
  $("#id_montoDesc").attr("type","number");
  $("#id_montoDesc").val(parseFloat(valmd.replace(/,/g,"")));
  $("#id_montoDesc").val(parseFloat($("#id_montoDesc").val()).toFixed(2));
  

  const valmq=$("#id_montoAceptado").val();
  $("#id_montoAceptado").attr("type","number");
  $("#id_montoAceptado").val(parseFloat(valmq.replace(/,/g,"")));
  $("#id_montoAceptado").val(parseFloat($("#id_montoAceptado").val()).toFixed(2));
 // $("#id_montoAceptado").prop('disabled', false);
  
  const valmeo=$("#id_montoEjecutado").val();
  $("#id_montoEjecutado").attr("type","number");
  $("#id_montoEjecutado").val(parseFloat(valmeo.replace(/,/g,"")));
  $("#id_montoEjecutado").val(parseFloat($("#id_montoEjecutado").val()).toFixed(2));
  //$("#id_montoEjecutado").prop('disabled', false);

  const valmee=$("#id_montoPorEjecutarse").val();
  $("#id_montoPorEjecutarse").attr("type","number");
  $("#id_montoPorEjecutarse").val(parseFloat(valmee.replace(/,/g,"")));
  $("#id_montoPorEjecutarse").val(parseFloat($("#id_montoPorEjecutarse").val()).toFixed(2));
 // $("#id_montoPorEjecutarse").prop('disabled', false);
  
});