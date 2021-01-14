var p_url = "";

window.onload = function() {

  var e = document.getElementById("seleccion");
	var text = e.options[e.selectedIndex].text;	

	if (text!="Tarjeta de Crédito"){
    document.getElementById("asterisco").style.display='none';
    document.getElementById("id_emisoraTarjeta").classList.remove("requiredField");

	}
	else{
    document.getElementById("asterisco").style.display='inline';
    document.getElementById("id_emisoraTarjeta").classList.add("requiredField");

	}
};

function run(){
	var e = document.getElementById("seleccion");
	var text = e.options[e.selectedIndex].text;	

	if (text!="Tarjeta de Crédito"){
    document.getElementById("asterisco").style.display='none';
    document.getElementById("id_emisoraTarjeta").classList.remove("requiredField");
  }
  else{
    document.getElementById("asterisco").style.display='inline';
    document.getElementById("id_emisoraTarjeta").classList.add("requiredField");

  }
}	


function load_ordenes_facturas(){
  // var opcion1 = $('<option value="primero">primero</option>')
  // $('#prueba').html(opcion1);
  var link = $('#form-fact').attr("orden-facturacion-url");
  console.log(link);
  $.ajax({
    url: link,
    success: function (data) {
      console.log(data.ordenes_facturacion);
      $("#prueba").html(data.ordenes_facturacion);
    }
  });
}



$('.select2').select2({
  minimumInputLength: 2,
  width: '100%' ,
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

function load_data(url, persona) {
  var url = $('#form-fact').attr("data-persona-url");
  var persona = $("#id_tipo_cliente").val();
  if (persona != "") {
    var url = url
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
        // $('#select2-id_ruc_ci-container').text($('#rc').val());
        // $('#select2-id_razon_nombres-container').text($('#rn').val());
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
  }
  else {
    $('#field-razon').hide();
    $('#field-ruc-ci').hide();
  }
};

function autocomplete(from, to) {
  if (from.val() != "") {
    $('#' + to).val($('#' + to + " option[name='" + from.val() + "']").val());
    $('#select2-' + to + '-container').text($('#' + to).val());
  }
  else {
    $('#' + to).val("");
    $('#select2-' + to + '-container').text("---------");
  }
}


function cambiar_url(){
  $('#div_id_orden_facturacion').click(function (e) { 
    p_url = $('#form-fact').attr("ordenfact-url");
    console.log(p_url);
    
  });
}

$(document).ready(function () {
  cambiar_url();
});

load_data();


$("#id_tipo_cliente").on("change", load_data);

$('#id_razon_nombres').on('change', function () {
  autocomplete($(this), 'id_ruc_ci');
})




$('#id_ruc_ci').on('change', function () {
  autocomplete($(this), 'id_razon_nombres');
})

$(document).on('change','.select2-participantes',function(){
  var clickedselect=$(this).val();
  var id=$(this).attr('id');
  $('.select2-participantes').each(function(e){
    if($(this).attr('id')!=id){
      if($(this).val()==clickedselect){
        $(this).val("None").trigger('change');
      }
    }
  });
});

$(document).on('change','.select2-participantes',function(){
  var clickedselect=$(this).val();
  var id=$(this).attr('id');
  $('.select2-participantes').each(function(e){
    if($(this).attr('id')!=id){
      if($(this).val()==clickedselect){
        $(this).val("None").trigger('change');
      }
    }
  });
});


//$('document').ready(function(){});

$(document).ready(function(){
  var parts = window.location.pathname.split('/');
  var lastSegment = parts.pop() || parts.pop();  // handle potential trailing slash

  var integer = parseInt(lastSegment, 10);

  if(!isNaN(integer)){
    var url = $('#form-fact').attr("data-orden-url");
    var persona = $("#id_tipo_cliente").val();
    if (persona != "") {
      var url = url
      $.ajax({
        url: url,
        data: {
          'pk': integer,
        },
        success: function (data) {
            $("#id_ruc_ci").val( data.ci.toString(10));
            $('#select2-id_ruc_ci-container').text($('#id_ruc_ci').val());
            $("#id_ruc_ci").trigger('change')
        }
      });

    }

  }
  
});