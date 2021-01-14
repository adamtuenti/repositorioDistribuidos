var p_url = "";
console.log("valor de la wea "+$('#cont').val())

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

$('.select3').select2({
  minimumInputLength: 0,
  width: '100%',
  language: {

    noResults: function () {
      return "No hay resultados";
    },
    searching: function () {

      return "Buscando...";
    }
    // ,
    // inputTooShort: function (e) {
    //   var t = e.minimum - e.input.length;
    //   return "Ingresa " + t + " caractéres para buscar";
    // }
  }
});

function load_info() {
  var url = $('#form-fact').attr("data-info-url");
  console.log($("#id_cod_orden_fact").val());
  if($("#id_cod_orden_fact").val()===""){
    var id= $('#id_ruc_ci').val();
  }else if(flag){
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
      if( $("#id_tipo_cliente").val()=="Natural"){
        console.log("entro a natural")
        
        $("#telefono").val(data.telefono);
        $("#direccion").val(data.direccion);
        $("#email").val(data.email);
        
      }else if($("#id_tipo_cliente").val()=="Jurídica"){
        $("#telefono").val(data.telefono);
        $("#direccion").val(data.direccion);
        $.ajax({
          url: $('#form-fact').attr("data-contacto-url"),
          data: {
            'id': id
          },
          success: function (data) {
            $("#id_contacto").html(data.contacto);
            $("#id_contacto").prop("disabled",false);
            if($('#cont').val()!=undefined){
              $('#id_contacto').val($('#cont').val());
              $('#id_contacto').trigger('change');
            }
            
          }
        });

      }
      
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
        console.log(data)
        $("#id_ruc_ci").html(data.ruc_ci)
        $("#id_razon_nombres").html(data.razon_nombre)
        $('#id_ruc_ci').val($('#rc').val());
        $('#id_razon_nombres').val($('#rn').val());
        $('#id_ruc_ci').trigger('change.select2');
        $('#id_razon_nombres').trigger('change.select2');
        //$('#select2-id_ruc_ci-container').text($('#rc').val());
        //$('#select2-id_razon_nombres-container').text($('#rn').val());
      }
    });
    $('#field-razon').show();
    $('#field-ruc-ci').show();

    if (persona == "Natural") {
      $('#ruc_ci').text('CI');
      $('#ra_nom').text('Nombre');
      $("#id_contacto").prop("disabled",true);
      $("#id_contacto").html("");
      p_url = $('#form-fact').attr("data-natural-url");
    }
    else if (persona == "Jurídica") {
      $('#ruc_ci').text('RUC');
      $('#ra_nom').text('Razón Social');
      $("#id_contacto").prop("disabled",true)
      p_url = $('#form-fact').attr("data-juridica-url");
    }
    $("#id_contacto").html("");
    $("#telefono").val("");
    $("#direccion").val("");
    $("#email").val("");
  }
  else {
    $("#id_contacto").prop("disabled",true)
    $('#field-razon').hide();
    $('#field-ruc-ci').hide();
    $("#id_contacto").html("");
    $("#telefono").val("");
    $("#direccion").val("");
    $("#email").val("");
  }
};

function load_mail() {
  console.log("entro al mail")
  var url = $('#form-fact').attr("data-mail-url");
  console.log(url)
  var cedula ="";
  if($("#id_contacto").val()!=undefined){
    cedula = $("#id_contacto").val().split("-")[0];
  }else{
    cedula = $("#cont").val().split("-")[0];
  }
    $.ajax({
      url: url,
      data: {
        'cedula': cedula
      },
      success: function (data) {
        $("#email").val(data.email);
      }
    });
    
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

$(document).on('change', '#id_contacto', function () {
  load_mail();
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
  $("#id_contacto").html("");
  load_data();
});

$(document).on('click', "#div_id_razon_nombres span.selection", function (e) {
  $("#rc").val("");
  $("#rn").val("");
  $("#id_contacto").html("");
  load_data();
});


//Asesor
console.log($("#id_asesor").attr("readonly"));
if($("#id_asesor").attr("readonly")!="readonly"){
  $.ajax({
    url: $('#form-fact').attr("data-asesor-url"),
    data: {
      'persona': ""
    },
    success: function (data) {
      console.log(data)
      $("#id_asesor").html(data.asesores);
      $('#id_asesor').val($('#as').val());
    }
  });
}

if($("#est").val()=="ANLD"){
    $("#id_n_factura").prop("readonly",true);
    $("#id_fecha_factura").prop("readonly",true);
    $("#id_anexo_factura").prop("disabled",true)
}
